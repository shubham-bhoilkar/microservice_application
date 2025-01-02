from fastapi import FastAPI , HTTPException
from models import create_user ,update_user
from user_api_function import register_user_logic, view_records_logic ,update_user_logic ,delete_user_logic

import logging

app = FastAPI()

logger = logging.getLogger("user_microservice")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"),logging.StreamHandler()])

@app.get("/")
def main_page():
    return {"Welcome":"Here comes your demo home page"}

@app.post("/register")
def register_user(user: create_user):
    try:
#        logger.info("Registration api request.")
        result = register_user_logic(user, logger)

        if result:
            return {"status": "success", "message":"User created sucessfully" }
        else:
            return {"status": "failure", "message":"User creatoin failed." }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code= 500, detail="Internal Server Error.")

@app.get("/get_user_details")
def get_user_details(user_id: int):
    try:
        #value user_id passing to user_api_function
        records = view_records_logic(user_id, logger)
        
        if records:
            return {"status": "success", "data": records}
        else:
            return {"status": "failure", "data": []}
        
    except Exception as e:
        logger.error(f"Error reading records from table 'user_details': {e}")
        raise HTTPException(status_code=500, detail=f"Error reading records from table 'user_details'.")

@app.post("/update_user_details")
def update_user_details(user: update_user):
    try:
        result = update_user_logic(user, logger)
        if result:
            return {"status": "success", "message": "user details updated."}
        else:
            return {"status": "failure", "message": "user detail update failed."}
            
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code = 500, detail="Internal Server Error.")

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    try:
        result = delete_user_logic(user_id, logger)
        
        if result:
            return {"status": "success", "message": f"User with user_id {user_id} has been deleted."}
        else:
            return {"status": "failure", "message": f"No user found with user_id {user_id}."}
        
    except Exception as e:
        logger.error(f"Error deleting user with user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app,host="0.0.0.0", port=50001)