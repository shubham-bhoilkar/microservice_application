from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import User

# Global Database Configuration
DATABASE_URL = "mysql+pymysql://root:neural123@10.10.7.64:3306/mydatabase"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

# Generic CRUD Operations with Exception Handling and Logging
def execute_query(query: str, params=None, log=None):
    try:
        with Session() as session:
            if log:
                log.info(f"Executing query: {query} with params: {params}")
            result = session.execute(query, params or {})
            session.commit()
            return result
    except SQLAlchemyError as e:
        if log:
            log.error(f"Query failed: {query} with params: {params}. Error: {e}")
        raise RuntimeError(f"Database operation failed: {e}") from e

#api created and available
def create_record(table_name: str, data: dict, log=None):
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        execute_query(query, data, log)
        if log:
            log.info(f"Record created in table '{table_name}': {data}")
    except Exception as e:
        if log:
            log.error(f"Failed to create record in table '{table_name}': {data}. Error: {e}")
        raise

#api pending/ completed
def read_records(table_name: str, filters=None, log=None):
    try:
        base_query = f"SELECT * FROM {table_name}"
        
        if filters:
            filter_clauses = " AND ".join(f"{key} = :{key}" for key in filters.keys())
            base_query += f" WHERE {filter_clauses}"
        
        if log:
            log.info(f"Reading records from table '{table_name}' with filters: {filters}")
        
        with Session() as session:
            result = session.execute(base_query, filters or {}).fetchall()
            return result
    except Exception as e:
        if log:
            log.error(f"Failed to read records from table '{table_name}' with filters: {filters}. Error: {e}")
        raise

#api pending
def update_record(table_name: str, record_id: int, id_column: str = "id", data: dict = None, log=None):
    try:
        set_clause = ", ".join(f"{key} = :{key}" for key in data.keys())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = :id"
        params = {**data, "id": record_id}
        execute_query(query, params, log)
        if log:
            log.info(f"Record updated in table '{table_name}' with ID {record_id}: {data}")
    except Exception as e:
        if log:
            log.error(f"Failed to update record in table '{table_name}' with ID {record_id}: {data}. Error: {e}")
        raise

#api pending
def delete_record(table_name: str, record_id: int, id_column: str = "id", log=None):
    try:
        query = f"DELETE FROM {table_name} WHERE {id_column} = :id"
        execute_query(query, {"id": record_id}, log)
        if log:
            log.info(f"Record deleted from table '{table_name}' with ID {record_id}")
    except Exception as e:
        if log:
            log.error(f"Failed to delete record from table '{table_name}' with ID {record_id}. Error: {e}")
        raise

#api pending
def initialize_table(table_name: str, schema: str, log=None):
    try:
        with engine.connect() as connection:
            if log:
                log.info(f"Initializing table '{table_name}' with schema: {schema}")
            connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
    except Exception as e:
        if log:
            log.error(f"Failed to initialize table '{table_name}'. Error: {e}")
        raise


# Example Usage
if __name__ == "__main__":
    # Initialize a table
    table_name = "users"
    # Create a record
    create_record(table_name, {"name": "Alice", "age": 25})

    # Read records
    users = read_records(table_name)
    print(f"Users: {users}")

    # Update a record
    update_record(table_name, record_id=1, data={"name": "Alice Smith", "age": 26})

    # Read updated records
    updated_users = read_records(table_name, {"id": 1})
    print(f"Updated User: {updated_users}")

    # Delete a record
    delete_record(table_name, record_id=1)
