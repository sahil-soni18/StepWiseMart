from pydantic import BaseModel
from typing import  Optional
from datetime import datetime

class CartBase(BaseModel):
    user_id: int
    items: Optional[dict] = {} # List of dictionaries representing cart items
    total_price: int = 0

class CartCreate(CartBase):
    user_id: int  # Used for creating a cart


class CartUpdate(BaseModel):
    user_id: Optional[int]
    items: Optional[dict] = {}
    total_price: Optional[int]


    class Config:
        from_attributes = True

class CartOut(CartBase):
    id: int
    # user_id: int
    # items: Optional[List[dict]] = []  # Same as above, to hold cart items as a list of dicts.
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
