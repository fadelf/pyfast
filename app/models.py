from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    age = Column(Integer)
    is_active = Column(Boolean)
