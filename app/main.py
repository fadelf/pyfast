from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, Response
import requests
import pandas as pd
import json

from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

from models import UserModel, ProductModel

import matplotlib.pyplot as plt
from io import BytesIO

from auth import AuthHandler
from schemas import UserRegister, UserLogin, ProductCreate, ProductUpdate
from metadata import tags_metadata

myapp = FastAPI(openapi_tags=tags_metadata)
auth_handler = AuthHandler()

# create all tables if not exist
Base.metadata.create_all(engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@myapp.post("/product/add", status_code=200, tags=["product"])
async def create_product(product: ProductCreate, db: Session = Depends(get_db),
                         username=Depends(auth_handler.auth_wrapper)):
    product_model = ProductModel(
        name=product.name,
        category=product.category,
        price=product.price,
        is_active=product.is_active)
    db.add(product_model)
    db.commit()
    db.refresh(product_model)
    return {"status": "Success", "result": product_model}


@myapp.put("/products/update/{product_id}", status_code=200, tags=["product"])
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db),
                         username=Depends(auth_handler.auth_wrapper)):
    # noinspection PyTypeChecker
    product_model = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.name:
        product_model.name = product.name
    if product.category:
        product_model.category = product.category
    if product.price:
        product_model.price = product.price
    if product.is_active is not None:
        product_model.is_active = product.is_active
    db.commit()
    db.refresh(product_model)
    return {"status": "Success", "result": product_model}


@myapp.get("/product/get/{product_id}", status_code=200, tags=["product"])
async def read_product(product_id: int, db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    # noinspection PyTypeChecker
    product_model = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "Success", "result": product_model}


@myapp.delete("/product/delete/{product_id}", status_code=200, tags=["product"])
async def delete_product(product_id: int, db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    # noinspection PyTypeChecker
    product_model = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_model)
    db.commit()
    return {"status": "Success", "result": f"Product {product_id} deleted by {username}"}


@myapp.post("/register", status_code=200, tags=["user"])
def register(user: UserRegister, db: Session = Depends(get_db)):
    lowercase_email = user.email.lower()
    # noinspection PyTypeChecker
    user_check = db.query(UserModel).filter(UserModel.email == lowercase_email).first()
    if user_check:
        raise HTTPException(status_code=400, detail="User with same email already exist")

    user_model = UserModel(
        username=user.username,
        email=user.email.lower(),
        password=auth_handler.get_password_hash(user.password),
        age=user.age,
        is_active=user.is_active)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"status": "Success", "result": None}


@myapp.post("/login", tags=["user"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    lowercase_email = user.email.lower()
    # noinspection PyTypeChecker
    user_check = db.query(UserModel).filter(UserModel.email == lowercase_email).first()

    if not user_check:
        raise HTTPException(status_code=404, detail=f"User with email {lowercase_email} not found")

    if not auth_handler.verify_password(user.password, user_check.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = auth_handler.encode_token(user_check.email)
    return {
        "token": token
    }


@myapp.get("/", tags=["test"])
def welcome_page():
    return {
        "message": "Fast API Development Home Page"
    }


@myapp.get("/weather", tags=["weather"])
async def weather(city: str, api_key: str = Header(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key is required")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("message"))

    return response.json()


@myapp.post("/convert", tags=["dataset"])
async def convert_csv(file: UploadFile):
    data_frame = pd.read_csv(file.file)

    json_data = json.loads(data_frame.to_json(orient="records"))

    return {
        "data": json_data
    }


@myapp.get("/plot", tags=["dataset"])
async def plot():
    x_values = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    y_values = [100, 125, 75, 175, 200, 100, 100]

    plt.plot(x_values, y_values)
    plt.title("Sample Matplotlib")
    plt.xlabel("Days")
    plt.ylabel("Values")

    # Matplotlib to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = buffer.getvalue()

    # Response as image
    response = Response(content=plot_data, media_type="image/png")

    return response
