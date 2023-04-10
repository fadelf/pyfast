from pydantic import BaseModel, validator
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    age: int
    is_active: bool = True


class UserLogin(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_must_not_be_empty(cls, email):
        if email.strip() == '':
            raise ValueError('Email must not be empty')
        return email

    @validator('password')
    def password_must_not_be_empty(cls, password):
        if password.strip() == '':
            raise ValueError('Password must not be empty')
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return password


class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
