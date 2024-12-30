import sqlite3
from fastapi import HTTPException
import logging
from configparser import ConfigParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    conn = sqlite3.connect('user.db')
    return conn

def register_user(user):
    try:
        username = user.username
        password = user.password

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('select * from users where username = ?', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        cursor.execute('insert into users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return {"message": "User registered successfully"}
    
    except HTTPException as e:
        logger.error(f"Error registering user: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
