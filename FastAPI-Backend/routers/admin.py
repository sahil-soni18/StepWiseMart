from fastapi import APIRouter, Depends, HTTPException
from models.Product import Product
from Schemas.ProductSchema import ProductBase, ProductCreate, ProductOut, ProductUpdate
from db.database import get_db, Session
from sqlalchemy.sql import func
from datetime import datetime, timezone
from Auth.Utils import JWTBearer

adminRouter = APIRouter()

# Admin Panel: Product APIs

# Add a new product (Admin Panel)

# Create a new product
@adminRouter.post("/products", response_model=ProductOut)
def create_product(product_data: ProductCreate, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):

    is_admin = token.get('is_admin')
    if not is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:

        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            image_urls=product_data.image_urls,
            colors=product_data.colors,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    except Exception as e:
        print(f"An error occurred while creating a product: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating a product")

# Update a product
@adminRouter.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    token: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    is_admin = token.get('is_admin')
    if not is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Fetch the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only provided fields
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    # Commit changes
    db.commit()
    db.refresh(product)
    return product

# Delete a product
@adminRouter.delete("/products/{product_id}")
def delete_product(product_id: int, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):

    is_admin = token.get('is_admin')
    if not is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product with ID {product_id} has been deleted successfully"}
