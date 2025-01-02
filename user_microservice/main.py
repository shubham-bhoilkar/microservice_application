from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from user_api_function import register_user_logic
from user_api_function import read_records
from models import User
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
def register_user(user: User):
    try:
        result = register_user_logic(user, logger)
    except Exception as e:
        # log error here
        # return specific reponse in case of failure
        print(f"Error: {e}")
        raise HTTPException(status_code= 500, detail="Internal Server Error.")

@app.get("/get_user_details/{user_id}")
def get_user_details(user_id: int, logger: logging.Logger):
    try:
        filter = {"user_id": user_id}
        
        #note here the parameters ae dirrectly going into the util_db.py rather than user_api_function.py and therfere once again tuscked that I am not using user_api_function.py file
        records = read_records("user_details", filter, logger)
        
        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "success", "data": []}
        
    except Exception as e:
        # Log the error and raise an HTTP exception
        logger.error(f"Error reading records from table 'user_details': {e}")
        raise HTTPException(status_code=500, detail=f"Error reading records from table 'user_details'.")
