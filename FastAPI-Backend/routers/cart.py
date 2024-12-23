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


# Add an item to the cart
@router.post("/cart")
async def add_to_cart(product_id: int, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    
    # Check if the product is already in the cart
    existing_item = next((item for item in cart if item["product_id"] == product_id), None)
    if existing_item:
        existing_item["quantity"] += quantity
    else:
        cart.append({"product_id": product_id, "quantity": quantity})
    
    return {"message": "Item added to cart", "cart": cart}

# View the cart
@router.get("/cart")
async def view_cart():
    if not cart:
        return {"message": "Cart is empty"}
    return {"cart": cart}

# Update an item in the cart
@router.put("/cart/{product_id}")
async def update_cart_item(product_id: int, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    
    item = next((item for item in cart if item["product_id"] == product_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart.")
    
    item["quantity"] = quantity
    return {"message": "Cart item updated", "cart": cart}

# Remove an item from the cart
@router.delete("/cart/{product_id}")
async def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item["product_id"] != product_id]
    return {"message": f"Item with product_id {product_id} removed from cart", "cart": cart}

# Clear the entire cart
@router.delete("/cart")
async def clear_cart():
    global cart
    cart = []
    return {"message": "Cart cleared", "cart": cart}
=======
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
>>>>>>> 34be854f1754c19c002f7d585d929e3b0753f29c
