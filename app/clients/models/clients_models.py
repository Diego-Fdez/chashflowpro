from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

# create a class model for create clients
class Client_Create(BaseModel):
    client_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

# create a class model for response clients
class Client_Model(BaseModel):
    id: uuid.UUID
    client_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True

# create a class model for update clients
class Client_Update(BaseModel):
    client_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None