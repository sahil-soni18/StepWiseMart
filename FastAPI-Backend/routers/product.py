# from fastapi import APIRouter,HTTPException

# # Create a router instance
# router = APIRouter()

# # Sample product data (for demonstration; replace with database integration)
# products = [
#     {"id": 1, "name": "Laptop", "price": 800, "stock": 10},
#     {"id": 2, "name": "Smartphone", "price": 500, "stock": 25},
# ]

# # Get all products
# @router.get("/product")
# async def get_all_products():
#     return {"products": products}

# # Get a product by ID
# @router.get("/product/{product_id}")
# async def get_product_by_id(product_id: int):
#     product = next((product for product in products if product["id"] == product_id), None)
#     if product:
#         return {"product": product}
#     return {"error": "Product not found"}

# # Add a new product
# @router.post("/product")
# async def create_product(name: str, price: float, stock: int):
#     new_product = {
#         "id": len(products) + 1,
#         "name": name,
#         "price": price,
#         "stock": stock,
#     }
#     products.append(new_product)
#     return {"message": "Product added successfully", "product": new_product}

# # Update a product
# @router.put("/product/{product_id}")
# async def update_product(product_id: int, name: str = None, price: float = None, stock: int = None):
#     product = next((product for product in products if product["id"] == product_id), None)
#     if not product:
#         return {"error": "Product not found"}
#     if name:
#         product["name"] = name
#     if price is not None:
#         product["price"] = price
#     if stock is not None:
#         product["stock"] = stock
#     return {"message": "Product updated successfully", "product": product}

# # Delete a product
# @router.delete("/product/{product_id}")
# async def delete_product(product_id: int):
#     global products
#     products = [product for product in products if product["id"] != product_id]
#     return {"message": f"Product with ID {product_id} deleted successfully"}


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models.Product import Product
from schemas.ProductSchema import ProductCreate, ProductOut
from db.database import get_db

router = APIRouter()

# Get all products
@router.get("/products", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# Get a single product by ID
@router.get("/products/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Create a new product
@router.post("/products", response_model=ProductOut)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        image_urls=product_data.image_urls,
        colors=product_data.colors,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Update a product
@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.image_urls = product_data.image_urls
    product.colors = product_data.colors
    product.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(product)
    return product

# Delete a product
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product with ID {product_id} has been deleted successfully"}
