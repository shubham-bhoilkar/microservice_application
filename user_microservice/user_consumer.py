from user_api_function import register_user_logic , update_user_logic , delete_user_logic
import nsq
import json
import configparser
import logging
from logging.handlers import RotatingFileHandler

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/python/microservice_application/config.ini')
log_file_path = config['Log']['file_path']

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


nsq_address = config['NSQ']['host']
nsq_port =config['NSQ']['port']

def nsq_subscription_handler(queue_name, callback,log):
    """
    Function to handle NSQ topic subscription.    
    Args:
        queue_name (str): The name of the queue to listen on.
        callback (function): The function that will process the messages.
    """
    
    def message_handler(message,log):
        """ This function is invoked when a message is received. """
        try:
            # Call the provided callback function with the message body.
            callback(message)
            # After processing the message, indicate successful handling.
            return message.ack()
        except Exception as e:
            log.error(f"Error processing message: {e}",exc_info =True)
            return message.requeue()

    # Create an NSQ reader to subscribe to the topic.
    reader = nsq.Reader(message_handler=message_handler,    # Handle the messages.
        topic=queue_name,            # The topic to subscribe to (change this as needed).
        channel="demo",                 # Use the provided queue name for the subscription.
        nsqd_tcp_addresses=[f'{nsq_address}:{4151}'],  # Provide NSQ server address.    
        max_in_flight=10 )                   # Max number of messages to be processed in parallel.


    # Run the reader to listen for incoming messages.
    try:
        # log.info(f"Subscribing to queue: {queue_name} on topic: 'your_topic_name'")
        nsq.run()
    except Exception as e:
        log.error(f"Error during NSQ subscription: {e}", exc_info=True)
        

def register_user(message,log):
    try:
        user_data = json.loads(message.body)

        success = register_user_logic(user_data, log)  # Assuming `log` is available globally or passed

        if success:
            log.info(f"User registration succesful, requeueing message.")
        else:
            log.error(f"Failed to register user, requeueing message.", exc_info =True)

    except Exception as e:
        log.error(f"Error processing message: {e}", exc_info=True)
        message.requeue()  # Requeue if any other exception occurs
        
def update_user_data(message,log):
    try:
        user_data = json.loads(message.body)

        success = update_user_logic(user_data, log)

        if success:
            log.info(f"User data update succesfully, requeueing message.")
        else:
            log.error(f"Failed to update user data, requeueing message.", exc_info =True)

    except Exception as e:
        log.error(f"Error processing message: {e}", exc_info =True)

def delete_user_data(message,log):
    try:
        user_data = json.loads(message.body)

        success = delete_user_logic(user_data, log)

        if success:
            log.info(f"User data deleted succesfully, requeueing message.")
        else:
            log.error(f"Failed to delete user data, requeueing message.",exc_info =True)

    except Exception as e:
        log.error(f"Error processing message: {e}", exc_info =True)


if __name__ == "__main__":
    queue_name = "register-user"
#    channel_name = "RegisterChannel"
    def consumer_topic():
        queue_name = input("Enter the topic name: ")
        if queue_name == "register-user" :
            nsq_subscription_handler(queue_name, register_user, logger)
        elif queue_name == "update-user" :
            nsq_subscription_handler(queue_name, update_user_data, logger)
        elif queue_name == "delete-user":
            nsq_subscription_handler(queue_name,delete_user_data, logger)
        else:
            logger.error(f"{queue_name} not found", exc_info =True)
        return True

    consumer_topic()        