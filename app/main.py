from fastapi import FastAPI, HTTPException
from typing import List
from models import User, UserData
from uuid import UUID, uuid4

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

@myapp.get("/api/user")
async def get_all_user():
    return userDb

@myapp.post("/api/user")
async def create_user(user: User):
    userDb.append(user)
    return {
        "id": user.id
    }

@myapp.delete("/api/user/{user_id}")
async def delete_user(user_id: UUID):
    for user in userDb:
        if user.id == user_id:
            userDb.remove(user)
            return f"Success delete user with ID {user_id}"
    raise HTTPException(
        status_code=404,
        detail=f"User with ID {user_id} not found!"
    )

@myapp.patch("/api/user/{user_id}")
async def update_user(user_id: UUID, userData: UserData):
    for user in userDb:
        if user.id == user_id:
            if userData.email is not None:
                user.email = userData.email
            return user
    raise HTTPException(
        status_code=404,
        detail=f"User with ID {user_id} not found!"
    )