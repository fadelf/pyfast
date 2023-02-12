from fastapi import FastAPI, HTTPException, Depends

from uuid import UUID
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

from data_models import User, UserData, UserBase, userList
from models import UserModel
from converter import base_to_user

tags_metadata = [
    {
        "name": "user",
        "description": "This API is connected to the database. The data remains while the database is running."
    },
    {
        "name": "user-example",
        "description": "This API is not connected to the database. The data will be reset every time the application is reloaded."
    },
    {
        "name": "test",
        "description": "This API is for testing to ensure the app runs correctly."
    }
]

myapp = FastAPI(openapi_tags=tags_metadata)

# create all tables if not exist
Base.metadata.create_all(engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@myapp.get("/", tags=["test"])
def welcome_page():
    return {
        "message" : "Fast API Development Home Page"
    }

@myapp.get("/api/user-example", tags=["user-example"])
async def list_user_example():
    return userList

@myapp.post("/api/user-example", tags=["user-example"])
async def add_user_example(user: User):
    userList.append(user)
    return {
        "id": user.id
    }

@myapp.delete("/api/user-example/{user_id}", tags=["user-example"])
async def delete_user_example(user_id: UUID):
    for user in userList:
        if user.id == user_id:
            userList.remove(user)
            return f"Success delete user with ID {user_id}"
    raise HTTPException(
        status_code=404,
        detail=f"User with ID {user_id} not found!"
    )

@myapp.patch("/api/user-example/{user_id}", tags=["user-example"])
async def update_user_example(user_id: UUID, userData: UserData):
    for user in userList:
        if user.id == user_id:
            if userData.email is not None:
                user.email = userData.email
            return user
    raise HTTPException(
        status_code=404,
        detail=f"User with ID {user_id} not found!"
    )

@myapp.post("/user/add", tags=["user"])
async def add_user(user: UserBase, db: Session = Depends(get_db)):
    user_model = base_to_user(user)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@myapp.get("/user/list", tags=["user"])
async def list_user(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users