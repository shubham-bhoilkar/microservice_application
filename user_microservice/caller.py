import nsq
import requests
from user_api_function import register_user_logic
import configparser

config = configparser.ConfigParser()
#config.read('/home/neural/workarea/Aaditya/python/microservice_application/user_microservice/config.ini')
config.read('/workspaces/sam_assignment/config.ini')

host =config ['NSQ']['host']
# nsqd_port =config['NSQ']['nsqd_port']
# nsqlookupd_port= config['NSQ']['nsqlookupd_port']


def register_user_caller(message, logger):
    try:
            # Define the NSQD HTTP endpoint
        nsqd_http_url = "http://10.10.7.64:4151/pub?topic=register-user"

        # Message payload
#        message = "Hello, NSQ!"

        # Send a POST request
        response = requests.post(nsqd_http_url, data=message)

        if response.status_code == 200:
            logger.info(f"Message published successfully!")
            return True
        else:
            logger.error(f"Failed to publish message:", response.status_code, exc_info =True)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return False

def update_user_caller(message, logger):
    try:
        writer = nsq.Writer(host)  # Address of NSQ producer
        writer.pub("update-user", message.encode('utf-8'))
        return True
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info = True)
        return False

def delete_user_caller(message, logger):
    try:
        writer = nsq.Writer(host)  # Address of NSQ producer
        writer.pub("regisetr-user", message.encode('utf-8'))
        return True
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info = True)
        return False
