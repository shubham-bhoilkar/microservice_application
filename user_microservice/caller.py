#import nsq
import requests
#from user_api_function import register_user_logic
import configparser

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/python/microservice_application/config.ini')
host = config['NSQ']['host']

def register_user_caller(message, logger):
    try:
        # Define the NSQD HTTP endpoint
        nsqd_http_url = "http://10.10.6.54:4171/pub?topic=register-user"  # Updated port to the default NSQD HTTP port (4171)

        # Send the POST request with the message
        response = requests.post(nsqd_http_url, data={"message": message})  # Message should be sent in a key-value pair

        if response.status_code == 200:
            logger.info("Message published successfully!")
            return True
        else:
            logger.error(f"Failed to publish message.", exc_info=True)
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while publishing the message.{e}", exc_info=True)
        return False
    
def update_user_caller(message,user_id, logger):
    try:
            # Define the NSQD HTTP endpoint
        nsqd_http_url = f"http://10.10.6.54:4171/pub?topic=update-user"

        payload = {"message":message,
                   "user_id":user_id}
        response = requests.post(nsqd_http_url, data={"update user message": payload})

        if response.status_code == 200:
            logger.info(f"Message published successfully!")
            return True
        else:
            logger.error(f"Failed to publish message:{e}", exc_info =True)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return False

def delete_user_caller(message, logger):
    try:
            # Define the NSQD HTTP endpoint
        nsqd_http_url = f"http://10.10.6.54:4171/pub?topic=delete-user"

        response = requests.post(nsqd_http_url, data={"message": message})

        if response.status_code == 200:
            logger.info(f"Message published successfully!")
            return True
        else:
            logger.error(f"Failed to publish message:{e}", exc_info =True)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return False
