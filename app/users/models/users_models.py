from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

# create a pydantic model for user
class User_Create(BaseModel):
    email: EmailStr
    sub: str
    username: str
    phone_number: Optional[str] = None

# model for user
class User_Model(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    phone_number: Optional[str] = None
    created_at: datetime
    is_active: bool
    is_admin: bool
    is_superuser: bool
    user_type: str
    is_pro: bool
    class Config:
        orm_mode = True

# model for Login User
class Login_User(BaseModel):
    access_token: str
    user: User_Model
    token_type: str

# model for update user
class Update_User(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    class Config:
        orm_mode = True