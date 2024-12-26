
from fastapi import APIRouter, Depends, HTTPException
from models.Cart import Cart
from Schemas.CartSchema import CartBase, CartCreate, CartOut, CartUpdate
from db.database import get_db, Session
from typing import List

cartRouter = APIRouter()
@cartRouter.post("/carts/", response_model=CartOut)
def create_new_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=cart.user_id, items=cart.items)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


@cartRouter.get("/carts/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart



#TODO:

# Update cart items
@cartRouter.put("/carts/{user_id}", response_model=CartOut)
def update_cart(user_id: int, cartData: CartUpdate, db: Session = Depends(get_db)):
    # Fetch the cart associated with the user
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Update fields dynamically
    for key, value in cartData.model_dump(exclude_unset=True).items():
        setattr(db_cart, key, value)
    
    db.commit()
    db.refresh(db_cart)
    return db_cart


@cartRouter.delete("/carts/{user_id}", response_model=bool)
def delete_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    raise HTTPException(status_code=404, detail="Cart not found")
