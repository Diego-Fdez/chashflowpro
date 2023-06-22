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


class User_Model(User_Create):
    id: uuid.UUID
    created_at: datetime
    is_active: bool
    is_admin: bool
    is_superuser: bool
    user_type: str
    is_pro: bool
    class Config:
        orm_mode = True