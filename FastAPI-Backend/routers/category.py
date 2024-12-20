from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/mydatabase"  # Update with your credentials
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ProductCategory model
class ProductCategory(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Create a router instance
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add a new product category
@router.post("/categories/add")
async def add_category(category_id: int, name: str, db: Session = Depends(get_db)):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
    # Check if the category already exists
    existing_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with the same ID already exists.")
    
    new_category = ProductCategory(id=category_id, name=name)
    db.add(new_category)
    db.commit()
    return {"message": "Category added", "category": {"id": new_category.id, "name": new_category.name}}

# View all product categories
@router.get("/categories/view")
async def view_categories(db: Session = Depends(get_db)):
    categories = db.query(ProductCategory).all()
    if not categories:
        return {"message": "No categories available"}
    return {"categories": [{"id": cat.id, "name": cat.name} for cat in categories]}

# Update an existing product category
@router.put("/categories/update/{category_id}")
async def update_category(category_id: int, name: str, db: Session = Depends(get_db)):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    category.name = name
    db.commit()
    return {"message": "Category updated", "category": {"id": category.id, "name": category.name}}

# Remove a product category
@router.delete("/categories/delete/{category_id}")
async def remove_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    db.delete(category)
    db.commit()
    return {"message": f"Category with ID {category_id} removed"}

# Clear all categories
@router.delete("/categories/clear")
async def clear_categories(db: Session = Depends(get_db)):
    db.query(ProductCategory).delete()
    db.commit()
    return {"message": "All categories cleared"}
