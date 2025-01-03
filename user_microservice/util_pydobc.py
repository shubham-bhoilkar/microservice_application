import pyodbc
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Global Database Configuration
CONNECTION_STRING = "DRIVER=MariaDB ODBC 3.1 Driver;SERVER=10.10.7.64;DATABASE=test_database;UID=root;PWD=neural123"

# Generic CRUD Operations with Exception Handling and Logging
def execute_query(query: str, params=None):
    try:
        log.info(f"Executing query: {query} with params: {params}")
        with pyodbc.connect(CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
    
                # Determine query type
                query_type = query.strip().split()[0].lower()

                if query_type == "select":  # READ
                    result = cursor.fetchall()
                    log.info(f"Query returned {len(result)} rows.")
                    return result

                conn.commit()
    except Exception as e:
        log.error(f"Query failed: {query} with params: {params}. Error: {e}")
        raise RuntimeError(f"Database operation failed: {e}") from e

# Create Record
def create_record(table_name: str, data: dict):
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        execute_query(query, tuple(data.values()))
        log.info(f"Record created in table '{table_name}': {data}")
    except Exception as e:
        log.error(f"Failed to create record in table '{table_name}': {data}. Error: {e}")
        raise

# Read Records
def read_records(table_name: str, filters=None):
    try:
        base_query = f"SELECT * FROM {table_name}"
        params = ()
        if filters:
            filter_clauses = " AND ".join(f"{key} = ?" for key in filters.keys())
            base_query += f" WHERE {filter_clauses}"
            params = tuple(filters.values())
        log.info(f"Reading records from table '{table_name}' with filters: {filters}")
        return execute_query(base_query, params)
    except Exception as e:
        log.error(f"Failed to read records from table '{table_name}' with filters: {filters}. Error: {e}")
        raise

# Update Record
def update_record(table_name: str, record_id: int, id_column: str = "id", data: dict = None):
    try:
        set_clause = ", ".join(f"{key} = ?" for key in data.keys())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
        params = (*data.values(), record_id)
        execute_query(query, params)
        log.info(f"Record updated in table '{table_name}' with ID {record_id}: {data}")
    except Exception as e:
        log.error(f"Failed to update record in table '{table_name}' with ID {record_id}: {data}. Error: {e}")
        raise

# Delete Record
def delete_record(table_name: str, filters: dict):
    try:
        filter_clauses = " AND ".join(f"{key} = ?" for key in filters.keys())
        query = f"DELETE FROM {table_name} WHERE {filter_clauses}"
        params = tuple(filters.values())
        execute_query(query, params)
        log.info(f"Record deleted from table '{table_name}' with filters: {filters}")
    except Exception as e:
        log.error(f"Failed to delete record from table '{table_name}' with filters: {filters}. Error: {e}")
        raise


if __name__ == "__main__":

    table_name = "user_details"
    # 1. Create records
    try:
        log.info("Performing Create operation...")
        create_record(table_name, {
            "first_name": "aditya",
            "last_name": "shetty",
            "phone": "7977672964",
            "email": "adityashetty35@gmail.com",
            "designation": "developer"
        })
        log.info("Record created successfully.")
    except RuntimeError as e:
        log.error(f"Failed to create record. Error: {e}")

    #2. Read records
    try:
        log.info("Performing Read operation...")
        records = read_records(table_name)
        log.info(f"Records retrieved: {records}")
    except RuntimeError as e:
        log.error(f"Failed to read records. Error: {e}")

    # 3. Update a record
    try:
        log.info("Performing Update operation...")
        update_record(table_name, record_id=2, id_column="user_id", data={
            "phone": "7977672964",
            "designation": "senior developer"
        })
        log.info("Record updated successfully.")
    except RuntimeError as e:
        log.error(f"Failed to update record. Error: {e}")

    # 4. Read updated records
    try:
        log.info("Retrieving updated records...")
        updated_records = read_records(table_name, {"user_id": 1})
        log.info(f"Updated Records: {updated_records}")
    except RuntimeError as e:
        log.error(f"Failed to retrieve updated records. Error: {e}")
