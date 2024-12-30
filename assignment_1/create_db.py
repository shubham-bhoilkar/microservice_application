import pyodbc

# Define connection parameters
db_name = "test_database"
host = "10.10.7.64"
user = "root"
password = "neural123"

# Define the ODBC connection string (using MariaDB ODBC driver 3.1)
connection_string = f"DRIVER={{MariaDB ODBC 3.1 Driver}};SERVER={host};DATABASE={db_name};USER={user};PASSWORD={password};"

# Create the connection
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
