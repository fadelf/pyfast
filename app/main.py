from fastapi import FastAPI

myapp = FastAPI()

@myapp.get("/")
def get_welcome_page():
    return {
        "message" : "Python API Developmet Home Page"
    }