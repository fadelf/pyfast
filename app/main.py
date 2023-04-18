import json
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, Response, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exception import CustomException

from sqlalchemy.orm import Session

from auth import AuthHandler
from database import Base, SessionLocal, engine
from metadata import tags_metadata
from models import UserModel, ProductModel
from schemas import UserRegister, UserLogin, ProductCreate, ProductUpdate

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


@myapp.post("/register", status_code=200, tags=["user"])
def register(user: UserRegister, db: Session = Depends(get_db)):
    lowercase_email = user.email.lower()
    # noinspection PyTypeChecker
    user_check = db.query(UserModel).filter(UserModel.email == lowercase_email).first()
    if user_check:
        raise CustomException("User with same email already exist")

    user_model = UserModel(
        username=user.username,
        email=user.email.lower(),
        password=auth_handler.get_password_hash(user.password),
        age=user.age,
        is_active=user.is_active)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    response_data = {
        "status_code": 200,
        "message": "Success",
        "result": None
    }
    return JSONResponse(content=response_data, status_code=200)


@myapp.post("/login", tags=["user"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    lowercase_email = user.email.lower()
    # noinspection PyTypeChecker
    user_check = db.query(UserModel).filter(UserModel.email == lowercase_email).first()

    if not user_check:
        raise CustomException("User not found!")

    if not auth_handler.verify_password(user.password, user_check.password):
        raise CustomException("Invalid password")
    token = auth_handler.encode_token(user_check.email)
    result = {
        "token": token
    }
    response_data = {
        "status_code": 200,
        "message": "Success",
        "result": result
    }
    return JSONResponse(content=response_data, status_code=200)


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
    response_data = {
        "status_code": 200,
        "message": "Success create",
        "result": f"Product ID: {product_model.product_id}"
    }
    return JSONResponse(content=response_data, status_code=200)


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
    response_data = {
        "status_code": 200,
        "message": "Success update",
        "result": f"Product ID: {product_model.product_id}"
    }
    return JSONResponse(content=response_data, status_code=200)


@myapp.get("/products", status_code=200, tags=["product"])
async def list_product(db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    products = db.query(ProductModel).all()
    return {
        "status_code": 200,
        "message": "Success retrieve",
        "result": products
    }


@myapp.get("/product/get/{product_id}", status_code=200, tags=["product"])
async def get_product(product_id: int, db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    # noinspection PyTypeChecker
    product_model = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status_code": 200,
        "message": "Success retrieve",
        "result": product_model
    }


@myapp.delete("/product/delete/{product_id}", status_code=200, tags=["product"])
async def delete_product(product_id: int, db: Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    # noinspection PyTypeChecker
    product_model = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product_model:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product_model)
    db.commit()
    response_data = {
        "status_code": 200,
        "message": "Success create",
        "result": f"Product {product_id} deleted by {username}"
    }
    return JSONResponse(content=response_data, status_code=200)


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
    data_frame = pd.read_csv(file.file, encoding="ISO-8859-1")

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


@myapp.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error = "Validation error: " + ", ".join([f"{err['msg']}" for err in errors])

    response_data = {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "message": "Failed",
        "result": {
            "error": error
        }
    }
    return JSONResponse(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)


@myapp.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        content={
            "status_code": exc.status_code,
            "message": exc.message,
            "result": exc.result,
        },
        status_code=exc.status_code,
    )


@myapp.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_detail = {
        "status_code": exc.status_code,
        "message": exc.detail,
        "result": None
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=error_detail,
    )
