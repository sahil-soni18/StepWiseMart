
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from models.Product import Product
from Schemas.ProductSchema import ProductOut, ProductCreate, ProductUpdate
from db.database import get_db

productRouter = APIRouter()

# Get all products
@productRouter.get("/products", response_model=List[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# Get a single product by ID
@productRouter.get("/products/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
