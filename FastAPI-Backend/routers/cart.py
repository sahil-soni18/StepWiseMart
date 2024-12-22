
from fastapi import APIRouter, Depends, HTTPException
from models.Cart import Cart
from Schemas.CartSchema import CartBase, CartCreate, CartOut
from db.database import get_db, Session
from typing import List

router = APIRouter()
@router.post("/carts/", response_model=CartOut)
def create_new_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=cart.user_id, items=cart.items)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


@router.get("/carts/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart



#TODO:

# Update cart items
# @router.put("/carts/{user_id}", response_model=CartOut)
# def update_cart(user_id: int, items: List[dict], db: Session = Depends(get_db)):
#     db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
#     if db_cart:
#         db_cart.items = items
#         db.commit()
#         db.refresh(db_cart)
#         return db_cart
#     raise HTTPException(status_code=404, detail="Cart not found")


@router.delete("/carts/{user_id}", response_model=CartOut)
def delete_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return db_cart
    raise HTTPException(status_code=404, detail="Cart not found")