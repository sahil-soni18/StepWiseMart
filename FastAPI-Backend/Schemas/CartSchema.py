from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartBase(BaseModel):
    user_id: int
    items: List[dict] = []  # List of dictionaries representing cart items

class CartCreate(CartBase):
    pass  # Used for creating a cart

class CartOut(CartBase):
    id: int
    # user_id: int
    # items: Optional[List[dict]] = []  # Same as above, to hold cart items as a list of dicts.

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
