from caller import register_user_caller
from user_api_function import register_user_logic
import nsq
import json
import configparser

config = configparser.ConfigParser()
#config.read('/home/neural/workarea/Aaditya/python/microservice_application/user_microservice/config.ini')
config.read('/workspaces/sam_assignment/user_microservice/config.ini')

nsqd_port =config['NSQ']['nsqd_port']
nsqlookupd_port= config['NSQ']['nsqlookupd_port']
# Set up the NSQ Consumer (subscriber) to listen to the 'register-user' topic
# def register_nsq_consumer(logger):
#     try:
#         # Set up the NSQ reader (consumer) to listen to the 'register-user' topic
#         nsq_reader = nsq.Reader(
#             message_handler=register_user_caller,  # The handler that will process each message
#             nsqd_tcp_addresses=nsqd_port,  # Update with your NSQ server address
#             topic='regisetr-user',  # The topic to subscribe to
#             channel='user-register-channel',  # The channel (should be unique)
#             lookupd_http_addresses=nsqlookupd_port  # Adjust if you're using NSQLookupd
#         )

#         # Start listening for messages from the NSQ topic
#         nsq.run() 
#         logger.info("NSQ Consumer started...")

#     except nsq.NSQError as nsq_error:
#         logger.error(f"NSQ error occurred: {nsq_error}", exc_info=True)
#     except Exception as e:
#         logger.error(f"Unexpected error while setting up NSQ Consumer: {e}", exc_info=True)


def nsq_subscription_handler(queue_name, callback):
    """
    Function to handle NSQ topic subscription.
    
    Args:
        queue_name (str): The name of the queue to listen on.
        callback (function): The function that will process the messages.
    """
    
    def message_handler(message):
        """ This function is invoked when a message is received. """
        try:
            # Call the provided callback function with the message body.
            callback(message)
            # After processing the message, indicate successful handling.
            return message.ack()
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return message.requeue()

    # Define the NSQ connection options.
    nsq_address = '127.0.0.1'  # NSQ server address, change this as necessary.
    nsq_port = 4150            # NSQ default port.

    # Create an NSQ reader to subscribe to the topic.
    reader = nsq.Reader(
        message_handler=message_handler,    # Handle the messages.
        topic='your_topic_name',            # The topic to subscribe to (change this as needed).
        channel=queue_name,                 # Use the provided queue name for the subscription.
        nsqd_tcp_addresses=[f'{nsq_address}:{nsq_port}'],  # Provide NSQ server address.
        max_in_flight=10                   # Max number of messages to be processed in parallel.
    )

    # Run the reader to listen for incoming messages.
    try:
        logging.info(f"Subscribing to queue: {queue_name} on topic: 'your_topic_name'")
        nsq.run()
    except KeyboardInterrupt:
        logging.info("Subscription interrupted by user.")
    except Exception as e:
        logging.error(f"Error during NSQ subscription: {e}")
        

def register_user(message,log):
    try:
        user_data = json.loads(message.body)

        success = register_user_logic(user_data, log)  # Assuming `log` is available globally or passed

        if success:
            log.info(f"User registration succesful, requeueing message.")
        else:
            log.error(f"Failed to register user, requeueing message.",exc_info =True)

    except json.JSONDecodeError as json_error:
        log.error(f"Error decoding JSON message: {json_error}", exc_info=True)
        message.requeue()  # Requeue if the message is malformed
    except Exception as e:
        log.error(f"Error processing message: {e}", exc_info=True)
        message.requeue()  # Requeue if any other exception occurs


if __name__ == "__main__":
    # Run the consumer
    # register_nsq_consumer()
    # read system argument and subscription to a topic and assign callback function
    queue_name = "register-user"

    if queue_name == "register-user":
        nsq_subscription_handler(queue_name, register_user)
    