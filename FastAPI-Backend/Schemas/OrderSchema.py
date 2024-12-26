from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    total_price: float
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "unpaid"

class OrderCreate(OrderBase):
    user_id: int  


class OrderUpdate(OrderBase):
    total_price: Optional[float]
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "unpaid"

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries
