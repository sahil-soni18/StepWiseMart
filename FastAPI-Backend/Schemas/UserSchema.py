from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .CartSchema import CartOut
from .OrderSchema import OrderOut

class UserBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    contact: str
    is_admin: bool = False  

class UserCreate(UserBase):
    password: str  # Password field for creating a user

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    contact: Optional[str] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None  # Password field for updating a user

class UserOut(UserBase):
    id: int
    cart: Optional[List['CartOut']] = []  # Optional relationship to cart
    orders: Optional[List['OrderOut']] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic will treat the SQLAlchemy models as dictionaries.

