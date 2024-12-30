from fastapi import FastAPI #, HTTPException, Depends
from pydantic import BaseModel
from user_api_function import UserAPI
import redis
#import logging

app = FastAPI()

r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register_user(user: User):
    return await UserAPI.register(user)

@app.post("/login")
async def login_user(user: User):
    return await UserAPI.login(user)

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return await UserAPI.get_user_info(user_id)

@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    return await UserAPI.update_user(user_id, user)

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    return await UserAPI.delete_user(user_id)
