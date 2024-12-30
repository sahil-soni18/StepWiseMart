from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class OrderProduct(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models


class OrderBase(BaseModel):
    total_price: float
    products: List[OrderProduct]
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "unpaid"

class OrderCreate(OrderBase):
    user_id: int  


class OrderUpdate(OrderBase):
    quantity: Optional[int] = None
    products: Optional[List[OrderProduct]] = None
    total_price: Optional[float] = None
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "unpaid"

class OrderOut(OrderBase):
    id: int
    user_id: int
    products: List[OrderProduct]
    status: str
    payment_status: str
    total_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries


