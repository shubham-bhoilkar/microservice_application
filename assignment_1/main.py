from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from user_api_function import register_user
from models import User

app = FastAPI()

@app.get("/")
def main_page():
    return {"Welcome":"Here comes your demo home page"}

@app.post("/register")
def register_user(user: User):
    try:
        result = register_user(user)
    except Exception as e:
        # log error here
        # return specific reponse in case of failure
        print(f"Error: {e}")
        raise HTTPException(status_code= 500, detail="Internal Server Error.")