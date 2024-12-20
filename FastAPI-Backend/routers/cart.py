from fastapi import APIRouter, HTTPException

# Create a router instance
router = APIRouter()

# Sample cart data (for demonstration; replace with database integration)
cart = []

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
