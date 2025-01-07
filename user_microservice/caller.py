import nsq
import json
from user_api_function import register_user_logic
import configparser

config = configparser.ConfigParser()
#config.read('/home/neural/workarea/Aaditya/python/microservice_application/user_microservice/config.ini')
config.read('/workspaces/sam_assignment/user_microservice/config.ini')

host =config ['NSQ']['host']
nsqd_port =config['NSQ']['nsqd_port']
nsqlookupd_port= config['NSQ']['nsqlookupd_port']

def register_user_caller(message, logger):
    try:
        writer = nsq.Writer(host)  # Address of NSQ producer
        writer.pub("regisetr-user", message.encode('utf-8'))
        return True
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info = True)
        return False
    
