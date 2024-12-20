from fastapi import APIRouter,HTTPException

# Create a router instance
router = APIRouter()

# Sample product data (for demonstration; replace with database integration)
products = [
    {"id": 1, "name": "Laptop", "price": 800, "stock": 10},
    {"id": 2, "name": "Smartphone", "price": 500, "stock": 25},
]

# Get all products
@router.get("/")
async def get_all_products():
    return {"products": products}

# Get a product by ID
@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return {"product": product}
    return {"error": "Product not found"}

# Add a new product
@router.post("/")
async def create_product(name: str, price: float, stock: int):
    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "stock": stock,
    }
    products.append(new_product)
    return {"message": "Product added successfully", "product": new_product}

# Update a product
@router.put("/{product_id}")
async def update_product(product_id: int, name: str = None, price: float = None, stock: int = None):
    product = next((product for product in products if product["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}
    if name:
        product["name"] = name
    if price is not None:
        product["price"] = price
    if stock is not None:
        product["stock"] = stock
    return {"message": "Product updated successfully", "product": product}

# Delete a product
@router.delete("/{product_id}")
async def delete_product(product_id: int):
    global products
    products = [product for product in products if product["id"] != product_id]
    return {"message": f"Product with ID {product_id} deleted successfully"}
