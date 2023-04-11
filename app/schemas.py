from pydantic import BaseModel, validator
from typing import Optional
import email_validator


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    age: int
    is_active: bool = True

    @validator('email')
    def email_must_not_be_empty(cls, email):
        if email.strip() == '':
            raise ValueError('Email must not be empty')
        return email

    @validator('email')
    def email_must_be_valid(cls, email):
        try:
            email_validator.validate_email(email)
        except email_validator.EmailNotValidError as e:
            raise ValueError('Invalid email') from e
        return email

    @validator('password')
    def password_must_not_be_empty(cls, password):
        if password.strip() == '':
            raise ValueError('Password must not be empty')
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return password


class UserLogin(BaseModel):
    email: str
    password: str


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
