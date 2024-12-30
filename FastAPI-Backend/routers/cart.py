# routers/cartRouter.py

from fastapi import APIRouter, Depends, HTTPException
from models.Cart import Cart, CartItem
from Schemas.CartSchema import CartCreate, CartOut, CartUpdate
from db.database import get_db, Session
from typing import List

cartRouter = APIRouter()

@cartRouter.post("/carts/", response_model=CartOut)
def create_new_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(
        user_id=cart.user_id, 
        total_price=cart.total_price
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    # Adding CartItems
    for item in cart.items:
        db_item = CartItem(cart_id=db_cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)
    db.commit()

    db.refresh(db_cart)
    return db_cart

@cartRouter.get("/carts/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

@cartRouter.put("/carts/{user_id}", response_model=CartOut)
def update_cart(user_id: int, cartData: CartUpdate, db: Session = Depends(get_db)):
    # Fetch the cart for the given user_id
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Update the cart fields except for the items (handled separately)
    for key, value in cartData.dict(exclude_unset=True).items():
        if key != "items":  # Skip updating the items here
            setattr(db_cart, key, value)
    
    # Handle items update (if provided in the request)
    if cartData.items is not None:
        # Clear existing items before adding the updated ones (optional)
        db_cart.items.clear()

        # Add new CartItem instances
        for item_data in cartData.items:
            new_item = CartItem(product_id=item_data.product_id, quantity=item_data.quantity)
            db_cart.items.append(new_item)

    # Commit the transaction and refresh the object to reflect changes
    db.commit()
    db.refresh(db_cart)
    
    return db_cart

'''
If required:

@cartRouter.put("/carts/{user_id}", response_model=CartOut)
def update_cart(user_id: int, cartData: CartUpdate, db: Session = Depends(get_db)):
    # Fetch the cart for the given user_id
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Update the cart fields except for the items (handled separately)
    for key, value in cartData.dict(exclude_unset=True).items():
        if key != "items":  # Skip updating the items here
            setattr(db_cart, key, value)
    
    # Handle items update (if provided in the request)
    if cartData.items is not None:
        for item_data in cartData.items:
            # Check if the product already exists in the cart
            existing_item = next((item for item in db_cart.items if item.product_id == item_data.product_id), None)
            if existing_item:
                # If the product exists, update the quantity
                existing_item.quantity = item_data.quantity
            else:
                # If the product doesn't exist, create a new CartItem and add it to the cart
                new_item = CartItem(product_id=item_data.product_id, quantity=item_data.quantity)
                db_cart.items.append(new_item)

    # Commit the transaction and refresh the object to reflect changes
    db.commit()
    db.refresh(db_cart)
    
    return db_cart
'''

@cartRouter.delete("/carts/{user_id}", response_model=bool)
def delete_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    raise HTTPException(status_code=404, detail="Cart not found")
