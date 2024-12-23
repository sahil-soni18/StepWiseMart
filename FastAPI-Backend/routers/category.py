# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session



# router = APIRouter()

# # Add a new product category
# @router.post("/categories/add")
# async def add_category(category_id: int, name: str, db: Session = Depends(get_db)):
#     if not name.strip():
#         raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
#     # Check if the category already exists
#     existing_category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
#     if existing_category:
#         raise HTTPException(status_code=400, detail="Category with the same ID already exists.")
    
#     new_category = ProductCategory(id=category_id, name=name)
#     db.add(new_category)
#     db.commit()
#     return {"message": "Category added", "category": {"id": new_category.id, "name": new_category.name}}

# # View all product categories
# @router.get("/categories/view")
# async def view_categories(db: Session = Depends(get_db)):
#     categories = db.query(ProductCategory).all()
#     if not categories:
#         return {"message": "No categories available"}
#     return {"categories": [{"id": cat.id, "name": cat.name} for cat in categories]}

# # Update an existing product category
# @router.put("/categories/update/{category_id}")
# async def update_category(category_id: int, name: str, db: Session = Depends(get_db)):
#     if not name.strip():
#         raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
#     category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found.")
    
#     category.name = name
#     db.commit()
#     return {"message": "Category updated", "category": {"id": category.id, "name": category.name}}

# # Remove a product category
# @router.delete("/categories/delete/{category_id}")
# async def remove_category(category_id: int, db: Session = Depends(get_db)):
#     category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found.")
    
#     db.delete(category)
#     db.commit()
#     return {"message": f"Category with ID {category_id} removed"}

# # Clear all categories
# @router.delete("/categories/clear")
# async def clear_categories(db: Session = Depends(get_db)):
#     db.query(ProductCategory).delete()
#     db.commit()
#     return {"message": "All categories cleared"}
