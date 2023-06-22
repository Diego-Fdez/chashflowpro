from pydantic import BaseModel
from typing import Optional
import uuid

# model for the token data
class TokenData(BaseModel):
    id: Optional[uuid.UUID] = None