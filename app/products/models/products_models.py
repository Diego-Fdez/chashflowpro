from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# create a pydantic model for create a product
class Product_Create(BaseModel):
    product_name: str
    price: float
    quantity: int
    description: Optional[str] = None
    category_id: uuid.UUID

# create a pydantic model for the response of a product

class Product_Model(Product_Create):
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID
    class Config:
        orm_mode = True

# create a pydantic model for update a product
class Product_Update(BaseModel):
    product_name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    description: Optional[str]
    category_id: Optional[uuid.UUID]