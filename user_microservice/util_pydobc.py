import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/python/microservice_application/config.ini')

host = config['Database']['host']
database = config['Database']['db_name']
driver = config['Database']['driver']
user = config['Database']['user']
password = config['Database']['password']
log_file_path = config['Log']['file_path']

# Global Database Configuration
CONNECTION_STRING = f"DRIVER={driver};SERVER={host};DATABASE={database};UID={user};PWD={password}"
#CONNECTION_STRING = "DRIVER=MariaDB ODBC 3.1 Driver;SERVER=10.10.6.54;DATABASE=sam_demo;UID=root;PWD=neural123"

# Generic CRUD Operations with Exception Handling and Logging
def execute_query(query: str, params=None,log=None):
    try:
        log.info(f"Executing query: {query} with params: {params}")
        with pyodbc.connect(CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())

                # Determine query type
                query_type = query.strip().split()[0].lower()

                if query_type == "select":  # READ
                    result = cursor.fetchall()
                    # Extract values from the result set
                    values = [tuple(row) for row in result]
                    log.info(f"Query returned {len(values)} rows.")
                    return values

                conn.commit()
                return True
    except Exception as e:
        log.error(f"Query failed: {query} with params: {params}. Error: {e}")
        raise RuntimeError(f"Database operation failed: {e}") from e

# Create Record
def create_record(table_name: str, data: dict,log = None):
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return execute_query(query, tuple(data.values()), log)
    except Exception as e:
        log.error(f"Failed to create record in table '{table_name}': {data}. Error: {e}")
        raise

# Read Records
def read_records(table_name: str, filters:dict,log =None):
    try:
        base_query = f"SELECT * FROM {table_name}"
        params = ()
        if filters:
            filter_clauses = " AND ".join(f"{key} = ?" for key in filters.keys())
            base_query += f" WHERE {filter_clauses}"
            params = tuple(filters.values())
        log.info(f"Reading records from table '{table_name}' with filters: {filters}")
        return execute_query(base_query, params, log)
    except Exception as e:
        log.error(f"Failed to read records from table '{table_name}' with filters: {filters}. Error: {e}")
        raise

# Update Record
def update_record(table_name: str, record_id: int, id_column: str = "user_id", data: dict = None,log =None):
    try:
        set_clause = ", ".join(f"{key} = ?" for key in data.keys())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
        params = (*data.values(), record_id)
        log.info(f"Record updated in table '{table_name}' with ID {record_id}: {data}")
        return execute_query(query, params,log)
    except Exception as e:
        log.error(f"Failed to update record in table '{table_name}' with ID {record_id}: {data}. Error: {e}")
        raise

# Delete Record
def delete_record(table_name: str, filters: dict,log = None):
    try:
        filter_clauses = " AND ".join(f"{value} = ?" for value in filters.values())
        query = f"DELETE FROM {table_name} WHERE {filter_clauses}"
        params = tuple(filters.values())
        log.info(f"Record deleted from table '{table_name}' with filters: {filters}")
        return execute_query(query, params,log)
        
    except Exception as e:
        log.error(f"Failed to delete record from table '{table_name}' with filters: {filters}. Error: {e}")
        raise
