from user_api_function import register_user_logic , update_user_logic , delete_user_logic
import nsq
import json
import configparser

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/python/microservice_application/config.ini')

nsq_address = config['NSQ']['host']
nsq_port =config['NSQ']['port']

def nsq_subscription_handler(queue_name,channel_name, callback,log):
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
    reader = nsq.Reader(
        message_handler=message_handler,    # Handle the messages.
        topic=queue_name,            # The topic to subscribe to (change this as needed).
        channel=channel_name,                 # Use the provided queue name for the subscription.
        nsqd_tcp_addresses=[f'{nsq_address}:{nsq_port}'],  # Provide NSQ server address.
        max_in_flight=10 )                   # Max number of messages to be processed in parallel.


    # Run the reader to listen for incoming messages.
    try:
        log.info(f"Subscribing to queue: {queue_name} on topic: 'your_topic_name'")
        nsq.run()
    except KeyboardInterrupt:
        log.info("Subscription interrupted by user.")
    except Exception as e:
        log.error(f"Error during NSQ subscription: {e}",exc_info=True)
        

def register_user(message,log):
    try:
        user_data = json.loads(message.body)

        success = register_user_logic(user_data, log)  # Assuming `log` is available globally or passed

        if success:
            log.info(f"User registration succesful, requeueing message.")
        else:
            log.error(f"Failed to register user, requeueing message.",exc_info =True)

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
            log.error(f"Failed to update user data, requeueing message.",exc_info =True)

    except Exception as e:
        log.error(f"Error processing message: {e}",exc_info =True)

def delete_user_data(message,log):
    try:
        user_data = json.loads(message.body)

        success = delete_user_logic(user_data, log)

        if success:
            log.info(f"User data deleted succesfully, requeueing message.")
        else:
            log.error(f"Failed to delete user data, requeueing message.",exc_info =True)

    except Exception as e:
        log.error(f"Error processing message: {e}",exc_info =True)


if __name__ == "__main__":
    # Run the consumer
    # register_nsq_consumer()
    # read system argument and subscription to a topic and assign callback function
    queue_name = "register-user"
    channel_name = "RegisterChannel"

    if queue_name == "register-user" and channel_name =="RegisterChannel":
        nsq_subscription_handler(queue_name,channel_name, register_user, None)
    elif queue_name == "-update_record" and channel_name== "UpdateChannel":
        nsq_subscription_handler(queue_name,channel_name, update_user_data, None)
    elif queue_name == "delete-user_record" and channel_name== "DeleteChannel":
        nsq_subscription_handler(queue_name, channel_name,delete_user_data, None)
    else:
#        log.error(f"{queue_name} not found")
        print(f"Topic: {queue_name} and Channel: {channel_name} not found.")