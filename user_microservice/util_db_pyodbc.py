import pyodbc
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection string
#DB_CONNECTION_STRING = "Driver={SQL Server};Server=10.10.7.64;Database=test_database;Trusted_Connection=yes;"
DB_CONNECTION_STRING = "mysql+pymysql://root:neural123@10.10.7.64:50001/test_database"
def get_db_connection() -> pyodbc.Connection:
#    Establishes and returns a database connection.
    try:
        logger.info("Request for Database connection.")
        connection = pyodbc.connect(DB_CONNECTION_STRING)
        logger.info("Database connection established successfully.")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise

def execute_query(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
#    Executes a read-only SQL query (e.g., SELECT) and returns results as a list of dictionaries.
    try:
        logger.info("Request for Query Execution.")
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        logger.info(f"Executed query successfully: {query}")
        return result
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise

def execute_non_query(query: str, params: Tuple = ()) -> int:
    """
    Executes an SQL query that does not return data (e.g., INSERT, UPDATE, DELETE).
    Returns the number of affected rows.
    """
    try:
        logger.info("Request for non-query execution.")
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        connection.close()
        logger.info(f"Executed non-query successfully: {query}")
        return affected_rows
    except Exception as e:
        logger.error(f"Error executing non-query: {e}")
        raise

def create_record(table: str, data: Dict[str, Any]) -> int:
#    Insert a record into the specified table.
    try:
        logger.info("Request to insert record.")
        columns = ", ".join(data.keys())
        values_placeholder = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholder})"
        params = tuple(data.values())
        return execute_non_query(query, params)
    except Exception as e:
        logger.error(f"Error occuring while inserting record: {e}")
        raise


def read_record(table: str, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
#    Read records from the specified table with optional conditions (e.g., WHERE).
    try:
        logger.info("Request to retrive data.")
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join([f"{key} = ?" for key in conditions])
        query = f"SELECT * FROM {table} {where_clause}"
        params = tuple(conditions.values()) if conditions else ()
        return execute_query(query, params)
    except Exception as e:
        logger.error(f"Error while retriving the data: {e}")
        raise

def update_record(table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
#    Update records in the specified table based on conditions.
    try:
        logger.info("Request to update record.")
        set_clause = ", ".join([f"{key} = ?" for key in data])
        where_clause = " AND ".join([f"{key} = ?" for key in conditions])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(data.values()) + tuple(conditions.values())
        return execute_non_query(query, params)
    except Exception as e:
        logger.error("Error while updating data.")
        raise
    
def delete_record(table: str, conditions: Dict[str, Any]) -> int:
#    Delete records from the specified table based on conditions.
    try:
        logger.info("Request to delete reocrd.")
        where_clause = " AND ".join([f"{key} = ?" for key in conditions])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        params = tuple(conditions.values())
        return execute_non_query(query, params)
    except Exception as e:
        logger.error("Error while delete record")
        raise