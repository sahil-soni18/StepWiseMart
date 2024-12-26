from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    order_id: int
    user_id: int
    amount: float
    payment_method: str = Field(..., description="The payment method used, e.g., 'Credit Card'")

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    status: str
    transaction_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
