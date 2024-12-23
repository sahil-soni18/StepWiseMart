from fastapi import APIRouter, Depends, HTTPException
from models.Product import Product
from Schemas.ProductSchema import ProductBase, ProductCreate, ProductOut
from db.database import get_db, Session
from sqlalchemy.sql import func

router = APIRouter()

# Admin Panel: Product APIs

# Add a new product (Admin Panel)
@router.post("/admin/products", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Retrieve all products (Admin Panel)
@router.get("/admin/products", response_model=list[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

# Retrieve a specific product by product ID (Admin Panel)
@router.get("/admin/products/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update product details (Admin Panel)
@router.put("/admin/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.stock = product.stock
        db_product.category = product.category
        db.commit()
        db.refresh(db_product)
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

# Delete a product (Admin Panel)
@router.delete("/admin/products/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")
