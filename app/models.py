from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    full_name: str
    email: str
    username: str
    is_active: bool = True