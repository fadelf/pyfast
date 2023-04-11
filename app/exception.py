from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(self, error_message: str):
        self.status_code = 400
        self.message = "Failed"
        self.result = {
            "error": f"{error_message}"
        }
