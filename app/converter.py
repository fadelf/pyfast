from data_models import UserData
from models import UserModel


def base_to_user(pydantic_model: UserData) -> UserModel:
    user_model = UserModel()
    user_model.username = pydantic_model.username
    user_model.email = pydantic_model.email
    user_model.age = pydantic_model.age
    user_model.is_active = pydantic_model.is_active
    return user_model
