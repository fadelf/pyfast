from fastapi import FastAPI
from typing import List
from models import User
from uuid import uuid4

myapp = FastAPI()

userDb: List[User] = [
    User(
        id=uuid4(),
        full_name="Cierra",
        username="cierra",
        email="cierra@gmail.com",
        is_active=True      
    ),
    User(
        id=uuid4(),
        full_name="Dinadan",
        username="dinadan",
        email="dinadan@gmail.com",
        is_active=True      
    )
]


@myapp.get("/")
def welcome_page():
    return {
        "message" : "Fast API Development Home Page"
    }

@myapp.get("/api/users")
async def get_users():
    return userDb