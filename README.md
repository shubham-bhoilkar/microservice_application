# Microservice CRUD Operations
This project demonstrates the creation of a simple microservice application that supports CRUD (Create, Read, Update, Delete) operations. The application is structured using Python, with separate modules handling specific tasks for clarity and scalability.

Microservice_Application

*main.py:* 

This is the entry point of the application. It initializes the API server and routes incoming requests to the appropriate handler functions. It interacts with the core logic of CRUD operations to process the requests and return the responses.

*user_api_function.py:*

This file contains helper functions that are specific to handling user-related API requests. It communicates with the util_db.py to perform database operations and contains the logic to handle the user data flow for each CRUD operation.

*util_pydobc.py:*

This file provides generic functions for performing CRUD operations. It contains functions to interact with the database (such as insert, read, update, and delete records), allowing the application to manage data efficiently. These functions are reusable across different modules for simplicity.

*config.ini:*

The configuration file holds environment-specific settings like database connections, server configurations, and API keys. This makes the project more adaptable, enabling different setups for development, testing, and production environments.

*requirements.txt:*

This file lists all the dependencies required to run the application, such as Flask, SQLAlchemy, and any other Python libraries used in the project. It allows for easy installation of the required libraries through pip.
