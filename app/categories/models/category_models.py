from pydantic import BaseModel
from datetime import datetime
import uuid

# model for create category

class Category_Create(BaseModel):
    category_name: str

class Category_Model(Category_Create):
    id: uuid.UUID
    created_at: datetime
    class Config:
        orm_mode = True