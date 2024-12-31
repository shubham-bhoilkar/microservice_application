'''
import logging

logging.basicConfig(level=logging.DEBUG, format ='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logging.debug("This is a debug message")
logging.info("This is an information message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
'''

import logging

# Create a logger
logger = logging.getLogger('my_logger')

# Create console handler and set level to WARNING
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Create file handler and set level to DEBUG
file_handler = logging.FileHandler('my_app.log')
file_handler.setLevel(logging.DEBUG)

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Log messages
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
