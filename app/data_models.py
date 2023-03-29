from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from typing import List


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    full_name: str
    email: str
    username: str
    is_active: bool = True


class UserBase(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    username: Optional[str]
    is_active: Optional[bool] = True


class UserData(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool


userList: List[User] = [
    User(
        id=uuid4(),
        full_name="Cierra",
        username="cierra",
        email="cierra@gmail.com",
        is_active=True
    ),
    User(
        id=uuid4(),
        full_name="Alsace",
        username="alsace",
        email="alsace@gmail.com",
        is_active=True
    )
]
