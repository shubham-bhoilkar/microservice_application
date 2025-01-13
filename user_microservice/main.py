from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
from models import create_user ,update_user 
from user_api_function import view_records_logic
from caller import register_user_caller , update_user_caller , delete_user_caller
from logging.handlers import RotatingFileHandler
import logging
import configparser
import redis
import json

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/python/microservice_application/config.ini')

host = config['Server']['host']
port = config['Server']['port']
log_file_path = config['Log']['file_path']

redis_client =redis.StrictRedis(host ='localhost', port =6379, db= 0)

def setup_logging(file_path):
    logger = logging.getLogger('user_microservice')
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )           
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logging(log_file_path)

app = FastAPI()

def get_from_cache(key: str):
    try:
        logger.info("Request to get the value from cache.")
        cached_value = redis_client.get(key)
        if cached_value :
            return json.loads(cached_value)
        return None
    except Exception as e:
        logger.error("Unable to get the value from cache. {e}", exc_info= True)

def set_to_cache(key: str, value: dict, ttl: int = 300):
    try:
        logger.info("Request to set the value from cache.")
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.error(f"Unable to set the value by key {key} in redis cache. {e}", exc_info =True)

def delete_from_cache(key: str):
    try:
        logger.info(f"Request to delete the key {key} from redis cache.")
        redis_client.delete(key)
    except Exception as e:
        logger.error(f"Unable to delete the key {key} from the redis cache. {e}",exc_info = True)

@app.get("/")
def main_page():
    return {"Welcome":"Here comes your demo home page"}

@app.post("/register")
def register_user(user: create_user):
    try:
        result = register_user_caller(user, logger)
        if result:
            set_to_cache(f"user:{user.user_id}", user.dict())
            return JSONResponse(
                status_code=201,
                content ={"status":"success","message":user})
        else:
            return JSONResponse(
                status_code=400,
                content ={"status":"failure", "message": "User Creation request not sent to NSQ."})
            
    except Exception as e:
        logger.error(f"Error during user registration: {e}",exc_info =True)
        raise HTTPException(status_code= 500, detail="Internal Server Error.")

@app.get("/get_user_details/{user_id}")
def get_user_details(user_id: int):
    try:
        cached_user =get_from_cache(f"user: {user_id}")
        if cached_user:
            return JSONResponse( status_code =200,
                                content= {"status": "success", "data":cached_user})
        records = view_records_logic(user_id, logger)
        
        if records:
            return JSONResponse(
                status_code=201,
                content= {"status": "success", "data": records}) 
        else:
            return JSONResponse(
                status_code=400,
                content={"status": "failure", "data": []})
        
    except Exception as e:
        logger.error(f"Error reading records from table 'user_details': {e}",exc_info =True)
        raise HTTPException(status_code=500, detail=f"Error reading records from table 'user_details'.")

@app.put("/update_user_details/{user_id}")
def update_user_details(user_id: int,user: update_user):
    try:
        result = update_user_caller(user, user_id, logger)
        if result:
            set_to_cache(f"user: {user_id}", user.dict())
            return JSONResponse(
                status_code=200,
                content ={"status": "success", "message": "user details updated."})
        else:
            return JSONResponse(
                status_code=400,
                content ={"status": "failure", "message": "user detail update failed."})
            
    except Exception as e:
        logger.error(f"Error during the update: {e}",exc_info =True)
        raise HTTPException(status_code = 500, detail="Internal Server Error.")

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    try:
        result = delete_user_caller(user_id, logger)
        
        if result:
            delete_from_cache(f"user: {user_id}")
            return JSONResponse(
                status_code=201,
                content={"status": "success", "message": f"User with user_id {user_id} has been deleted."})
        else:
            return JSONResponse(
                status_code=400,
                content={"status": "failure", "message": f"No user found with user_id {user_id}."})
        
    except Exception as e:
        logger.error(f"Error deleting user with user_id {user_id}: {e}",exc_info =True)
        raise HTTPException(status_code=500, detail="Internal Server Error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app,host=host, port=eval(port))