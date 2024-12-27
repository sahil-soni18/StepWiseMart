from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0 
    image_urls: Optional[List[str]] = []  
    colors: Optional[List[str]] = []  

class ProductCreate(ProductBase):
    pass  # Used for creating a new product

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    image_urls: Optional[List[str]]
    colors: Optional[List[str]]

    class Config:
        from_attributes = True

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
