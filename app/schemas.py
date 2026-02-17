from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class OrderBase(BaseModel):
    name: str
    description: Optional[str]
    quantity: Optional[int]
    price: Optional[Decimal]

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    # embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None   

class PredictionResponse(BaseModel):
    next_product: str
    reason: str
    suggested_quantity: int

    class Config:
        from_attributes = True
