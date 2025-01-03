from fastapi import FastAPI , HTTPException
from models import create_user ,update_user
from user_api_function import register_user_logic, view_records_logic ,update_user_logic ,delete_user_logic
import logging
from logging.handlers import RotatingFileHandler
import configparser

config = configparser.ConfigParser()
config.read('/workspaces/sam_assignment/user_microservice/config.ini')

host = config['Server']['host']
port = config['Server']['port']
log_file_path = config['Log']['file_path']


def setup_logging(file_path):
    logger.setLevel(logging.DEBUG)

    log_file_path = file_path
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.addHandler(file_handler)


    return logger

logger = setup_logging(log_file_path)

app = FastAPI()

@app.get("/")
def main_page():
    return {"Welcome":"Here comes your demo home page"}

@app.post("/register")
def register_user(user: create_user):
    try:
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
    uvicorn.run(app=app,host=host, port=port)