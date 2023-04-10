from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from database import Base


class UserModel(Base):
    """Represents a user in the system."""

    __tablename__ = "user"
    user_id: int = Column(Integer, primary_key=True, index=True, autoincrement=True, doc="The ID of the user.")
    username: str = Column(String, doc="The username of the user.")
    email: str = Column(String, unique=True, doc="The email of the user.")
    password: str = Column(String, doc="The password oh the user.")
    age: int = Column(Integer, doc="The age of the user.")
    is_active: bool = Column(Boolean, default=True, doc="Whether the user is active or not.")
    __table_args__ = (UniqueConstraint("username", "email", name="_user_uc"),)


class ProductModel(Base):
    """Represents a product in the system."""

    __tablename__ = "product"
    product_id: int = Column(Integer, primary_key=True, index=True, autoincrement=True, doc="The ID of the product.")
    name: str = Column(String, doc="The name of the product.")
    category: str = Column(String, doc="The category of the product.")
    price: float = Column(String, doc="The price of the product.")
    is_active: bool = Column(Boolean, default=True, doc="Whether the product is active or not.")
