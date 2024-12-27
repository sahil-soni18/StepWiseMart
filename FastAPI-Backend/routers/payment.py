import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.Payment import Payment
from models.Order import Order
from Schemas.PaymentSchema import PaymentCreate, PaymentOut

paymentRouter = APIRouter()

@paymentRouter.post("/payments", response_model=PaymentOut)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    # Simulate the payment process
    transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID

    # Check if the order exists
    order = db.query(Order).filter(Order.id == payment_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Create a new payment record
    payment = Payment(
        order_id=payment_data.order_id,
        user_id=payment_data.user_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        transaction_id=transaction_id,
        status="Success",  # Assume all payments are successful in simulation
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@paymentRouter.get("/payments/user/{user_id}", response_model=list[PaymentOut])
def get_user_payments(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this user")
    return payments


@paymentRouter.get("/payments/{transaction_id}", response_model=PaymentOut)
def get_payment_by_transaction(transaction_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
