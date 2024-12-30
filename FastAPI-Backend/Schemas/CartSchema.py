# Schemas/CartSchema.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartItem(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartBase(BaseModel):
    user_id: int
    total_price: float
    items: Optional[List[CartItem]] = []  # List of CartItem objects

    class Config:
        from_attributes = True

class CartCreate(CartBase):
    pass  # Used for creating a cart

class CartUpdate(BaseModel):
    user_id: Optional[int] = None
    items: Optional[List[CartItem]] = None  # List of CartItem objects
    total_price: Optional[float] = None

    class Config:
        from_attributes = True

class CartOut(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
