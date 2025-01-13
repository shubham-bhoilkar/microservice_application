from util_pydobc import create_record , read_records , update_record ,delete_record

def register_user_logic(user_data, log):
    try:
        log.info(f"Registraion request recived with user data {user_data}")
        data = {    
            "first_name": user_data.first_name,
            "last_name":user_data.last_name,
            "phone": user_data.phone,
            "email": user_data.email,
            "designation": user_data.designation }
        
        result = create_record("user_details", data, log)

        if result:
            log.info(f"User registered successfully at user_api_function.")
            return True
        else:
            log.error(f"User creation failed at user_api_function.", exc_info=True)
            return False

    except Exception as e:
        log.error(f"Error during creating user registration.{e}", exc_info = True)
        return False

def view_records_logic(user_data, log):
    try:
        log.info(f"Data view request by user: {user_data}")
        filter = {"user_id": user_data}
        result = read_records("user_details", filter, log)
        
        if result:
            log.info(f"User information retrieved successfully at user_api_function.")
            return result
        else:
            log.error(f"No user information found at user_api_function.")
            return "No Data Found."
        
    except Exception as e:
        log.error(f"Error retrieving user information: {e}", exc_info = True)
        return None

def update_user_logic(user_data,user_id, log):
    try:
        log.info(f"User data update request received by user: {user_data}")
        data = {
            "first_name":user_data.first_name ,
            "last_name":user_data.last_name ,
            "phone":user_data.phone ,
            "email":user_data.email ,
            "designation":user_data.designation 
        }
        
        result = update_record("user_details",user_id, "user_id",data,log)
        if result:
            log.info(f"User updated succesfully at user_api_function.")
        else:
            log.error(f"User updation failed at user_api_function.")
        return result
    except Exception as e:
        log.error(f"Error during updating user details.", exc_info = True)

def delete_user_logic(user_id: int, log):
    try:
        log.info(f"User data delete request received by user id: {user_id}")
        filters = {"user_id": user_id}
        result = delete_record("user_details", filters, log)
        
        return result
    
    except Exception as e:
        log.error(f"Error in delete_user_logic for user_id {user_id}: {e}", exc_info = True)
        raise e
