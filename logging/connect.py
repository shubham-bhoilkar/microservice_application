from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
#import logging

#logging.basicConfig(level=logging.DEBUG, format ='%(asctime)s - %(levelname)s - %(message)s',
#                    datefmt='%Y-%m-%d %H:%M:%S',
#                    handlers=[logging.StreamHandler()])

# Define the connection details
username = 'root'
password = 'neural123'
host = '10.10.7.64'  # or your server's IP
port = '3306'        # default MySQL port
database = 'test_database'

# Create the connection string
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

# Create the engine
engine = create_engine(connection_string)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to MySQL successfully!")

        # Define metadata
        metadata = MetaData()

        # Define a users table
        users_table = Table(
            'users',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('username', String(50), nullable=False),
            Column('email', String(100), nullable=False, unique=True),
            Column('age', Integer, nullable=True),
        )

        # Create the table in the database
        metadata.create_all(engine)
        print("Users table created successfully!")
    
        def create_user(username, email,age =None):
            try:
                new_user =users_table.insert().values(username =username, email= email)
                engine.execute(new_user)
                print("User Created Successfully!")
            except Exception as e:
                print(f"Error creating user: {e}")
                
        def get_user_by_id(user_id):
            try:
                query =users_table.select().where(users_table.c.id==user_id)
                result =engine.execute(query).fetchone()
                if result:
                    print(f"User Found: {result}")
                    return result
                else:
                    print("User not found")
                    return None
                
            except Exception as e:
                print(f"Error reading user: {e}")

        def update_user(user_id, username=None, email=None, age=None):
            try:
                update_query = users_table.update().where(users_table.c.id == user_id)
                
                # Apply changes if parameters are passed
                if username:
                    update_query = update_query.values(username=username)
                if email:
                    update_query = update_query.values(email=email)
                if age:
                    update_query = update_query.values(age=age)
                
                result = engine.execute(update_query)
                
                if result.rowcount > 0:
                    print("User updated successfully!")
                else:
                    print("No user found to update!")
            except Exception as e:
                print(f"Error updating user: {e}")
                
        def delete_user(user_id):
            try:
                delete_query = users_table.delete().where(users_table.c.id == user_id)
                result = engine.execute(delete_query)
                
                if result.rowcount > 0:
                    print("User deleted successfully!")
                else:
                    print("User not found!")
            except Exception as e:
                print(f"Error deleting user: {e}")

except Exception as e:
    print(f"Failed to connect to MySQL or create the table: {e}")

create_user("Shubham","shubham.b@neuralit.com",23)

get_user_by_id(1)

update_user("sam_bhoilkar","sam_bhoilkar@gmail.com",23)

delete_user(1)