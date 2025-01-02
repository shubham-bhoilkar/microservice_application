from util_db import create_record
from util_db import read_records
from util_db import update_record
from util_db import delete_record
# import logging

def register_user_logic(user_data, log):
    try:
        log.info(f"Registraion request recived with user data {user_data}")
        data = {    
            "first_name": user_data.first_name,
            "last_name":user_data.last_name,
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
        return False

    finally:
        return "registration action complete."

def view_records_logic(user_data, log):
    try:
        log.info(f"Data view request by user: {user_data}")
        filter = {"user_id": user_data.user_id}
        result = read_records("user_details", filter, log)
        
        if result:
            log.info(f"User information retrieved successfully for user_id {user_data.user_id}.")
            return result  # Return the user data or appropriate response
        else:
            log.error(f"No user information found for user_id {user_data.user_id}.")
            return "No Data Found."
        
    except Exception as e:
        log.error(f"Error retrieving user information: {e}")
        return None  # Return None in case of an error
    finally:
        log.info("User record retrieval action completed.")

def update_user_logic(user_data, log):
    try:
        log.info(f"User data update request received by user: {user_data}")
        data = {
            # "user_id":user_data.user_id,
            "first_name":user_data.first_name,
            "last_name":user_data.last_name,
            "phone":user_data.phone,
            "email":user_data.email,
            "designation":user_data.designation 
        }
        result = update_record("user_details",data.keys("user_id"),data)
        if result:
            log.info(f"User {user_data.user_id} updated succesfully.")
        else:
            log.error(f"User {user_data.user_id} updation failed.")
    except Exception as e:
        log.error(f"Error during updating user details.")
    finally:
        return "updation action complete."

def delete_user_logic(user_id: int, log):
    try:
        log.info(f"User data delete request received by user id: {user_id}")
        filters = {"user_id": user_id}
        result = delete_record("user", filters, log)
        
        return result
    
    except Exception as e:
        log.error(f"Error in delete_user_logic for user_id {user_id}: {e}")
        raise  
