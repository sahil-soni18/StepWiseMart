from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models.order import Order
from schemas.order_schema import OrderCreate, OrderOut
from db.database import get_db

router = APIRouter()

# Create a new order
@router.post("/orders", response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Create a new order
    new_order = Order(
        user_id=order_data.user_id,
        total_amount=order_data.total_amount,
        status=order_data.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

# Get an order by ID
@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Get all orders for a user
@router.get("/orders/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    db_orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return db_orders

# Update an order
@router.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_data: OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order details
    db_order.total_amount = order_data.total_amount
    db_order.status = order_data.status
    db_order.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_order)

    return db_order

# Delete an order
@router.delete("/orders/{order_id}", response_model=OrderOut)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()
    
    return db_order
