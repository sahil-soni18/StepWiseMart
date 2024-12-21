from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Create a router instance
router = APIRouter()

# In-memory storage
categories = []

# Pydantic models
class Category(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    id: int
    name: str

class CategoryUpdate(BaseModel):
    name: str

# Add a new product category
@router.post("/categories/add")
async def add_category(category: CategoryCreate):
    if not category.name.strip():
        raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
    # Check if the category already exists
    for existing_category in categories:
        if existing_category["id"] == category.id:
            raise HTTPException(status_code=400, detail="Category with the same ID already exists.")
    
    new_category = {"id": category.id, "name": category.name}
    categories.append(new_category)
    return {"message": "Category added", "category": new_category}

# View all product categories
@router.get("/categories/view")
async def view_categories():
    if not categories:
        return {"message": "No categories available"}
    return {"categories": categories}

# Update an existing product category
@router.put("/categories/update/{category_id}")
async def update_category(category_id: int, category: CategoryUpdate):
    if not category.name.strip():
        raise HTTPException(status_code=400, detail="Category name must not be empty.")
    
    for existing_category in categories:
        if existing_category["id"] == category_id:
            existing_category["name"] = category.name
            return {"message": "Category updated", "category": existing_category}
    
    raise HTTPException(status_code=404, detail="Category not found.")

# Remove a product category
@router.delete("/categories/delete/{category_id}")
async def remove_category(category_id: int):
    for index, existing_category in enumerate(categories):
        if existing_category["id"] == category_id:
            categories.pop(index)
            return {"message": f"Category with ID {category_id} removed"}
    
    raise HTTPException(status_code=404, detail="Category not found.")

# Clear all categories
@router.delete("/categories/clear")
async def clear_categories():
    categories.clear()
    return {"message": "All categories cleared"}
