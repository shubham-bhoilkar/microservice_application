from util_db import create_record
from util_db import read_records
# import logging

def register_user_logic(user_data, log):
    try:
        
        data = {    
            "username": user_data.username,
            "phone": user_data.phone,
            "email": user_data.email,
            "designation": user_data.designation }
        result = create_record("user", data, log)

        if result:
            log.info(f"User {user_data.username} with user id: {user_data.user_id} registered successfully.")
        else:
            log.error(f"User {user_data.username} with user id: {user_data.user_id} creation failed.")

        return True  # Registration success

    except Exception as e:
        log.error(f"Error during creating user registration.")

    finally:
        return "registration action complete."

#def read_records(table_name: str, filters=None, log=None):
def retrive_data(user_data, log):
    try:
        data={
            "user_id": user_data.user_id
        }
        result = read_records("user",data,log)
        
        if result:
            log.info(f"user information provided!")
        else:
            log.error(f"select query failed!")
        
    except Exception as e:
        log.error(f"user information not found!")
    finally:
        return "action complete with read records."