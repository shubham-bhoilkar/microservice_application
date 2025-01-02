from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from user_api_function import register_user_logic
from user_api_function import view_records_logic
from user_api_function import update_user_logic
from user_api_function import delete_user_logic
from models import create_user
from update_user_models import update_user

import logging

app = FastAPI()

logger = logging.getLogger("user_microservice")
logging.basicConfig(level=logging.INFO)

# Define the Pydantic model for the user registration request
class User(BaseModel):
    first_name: str
    last_name: str
    phone: int
    email: str
    designation: str

@app.get("/")
def main_page():
    return {"Welcome":"Here comes your demo home page"}

@app.post("/register")
def register_user(user: create_user):
    try:
        result = register_user_logic(user, logger)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code= 500, detail="Internal Server Error.")

@app.get("/get_user_details/{user_id}")
def get_user_details(user_id: int, logger: logging.Logger):
    try:
        #value user_id passing to user_api_function
        records = view_records_logic(user_id, logger)
        
        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "success", "data": []}
        
    except Exception as e:
        logger.error(f"Error reading records from table 'user_details': {e}")
        raise HTTPException(status_code=500, detail=f"Error reading records from table 'user_details'.")

@app.post("/update_user_details")
def update_user_details(user: update_user):
    try:
        result = update_user_logic(user, logger)
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code = 500, detail="Internal Server Error.")

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int, logger: logging.Logger):
    try:
        result = delete_user_logic(user_id, logger)
        
        if result:
            return {"status": "success", "message": f"User with user_id {user_id} has been deleted."}
        else:
            return {"status": "failure", "message": f"No user found with user_id {user_id}."}
        
    except Exception as e:
        logger.error(f"Error deleting user with user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
