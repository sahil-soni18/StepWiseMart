from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.Order import Order, OrderProduct
from Schemas.OrderSchema import OrderCreate, OrderOut, OrderUpdate
from db.database import get_db
from models.Product import Product  # Import the Product model

orderRouter = APIRouter()

# Create a new order

@orderRouter.post("/orders", response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Validate all product IDs exist
        for product in order_data.products:
            product_exists = db.query(Product).filter(Product.id == product.product_id).first()
            if not product_exists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product with ID {product.product_id} does not exist."
                )

        # Create a new order
        new_order = Order(
            user_id=order_data.user_id,
            total_price=order_data.total_price,
            status=order_data.status,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.add(new_order)
        db.flush()  # Get order ID before adding products

        # Add products to the order
        for product in order_data.products:
            order_product = OrderProduct(
                order_id=new_order.id,
                product_id=product.product_id,
                quantity=product.quantity
            )
            db.add(order_product)

        db.commit()
        db.refresh(new_order)

        return new_order

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

# Get an order by ID
@orderRouter.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Get all orders for a user
@orderRouter.get("/orders/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    db_orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return db_orders

# Update an order
@orderRouter.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order details
    for key, value in order_data.model_dump(exclude_unset=True).items():
        if key != "products":  # Skip products for now
            setattr(db_order, key, value)

    # Update products if provided
    if "products" in order_data.model_dump(exclude_unset=True):
        db.query(OrderProduct).filter(OrderProduct.order_id == db_order.id).delete()
        for product in order_data.products:
            db.add(OrderProduct(
                order_id=db_order.id,
                product_id=product.product_id,
                quantity=product.quantity
            ))

    db.commit()
    db.refresh(db_order)

    return db_order


# Delete an order
@orderRouter.delete("/orders/{order_id}", response_model=bool)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        db.delete(db_order)
        db.commit()
    
        return True
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
