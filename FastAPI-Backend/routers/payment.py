from fastapi import APIRouter, Depends, HTTPException
from models.Payment import Payment
from Schemas.PaymentSchema import PaymentBase, PaymentCreate, PaymentOut
from db.database import get_db, Session
import stripe

router = APIRouter()

# Stripe API key
stripe.api_key = "your_stripe_secret_key"

# Create a new payment using a payment gateway
@router.post("/payments/checkout", response_model=dict)
def create_payment_checkout(payment: PaymentCreate, db: Session = Depends(get_db)):
    try:
        # Create a payment intent with Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Amount in cents
            currency="usd",
            payment_method_types=["card"],
            metadata={"user_id": payment.user_id},
        )

        # Store payment details in the database
        db_payment = Payment(
            user_id=payment.user_id,
            amount=payment.amount,
            method="Stripe",
            status="Pending",
            payment_intent_id=payment_intent["id"]
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)

        return {"client_secret": payment_intent["client_secret"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")

# Handle webhook from the payment gateway
@router.post("/payments/webhook")
def stripe_webhook(payload: dict, db: Session = Depends(get_db)):
    endpoint_secret = "your_stripe_webhook_secret"

    try:
        sig_header = payload.headers["Stripe-Signature"]
        event = stripe.Webhook.construct_event(
            payload.body, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]

        # Update payment status in the database
        db_payment = db.query(Payment).filter(Payment.payment_intent_id == payment_id).first()
        if db_payment:
            db_payment.status = "Succeeded"
            db.commit()

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]

        # Update payment status in the database
        db_payment = db.query(Payment).filter(Payment.payment_intent_id == payment_id).first()
        if db_payment:
            db_payment.status = "Failed"
            db.commit()

    return {"status": "success"}
