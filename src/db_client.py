import pandas as pd
import psycopg
from psycopg import rows
import os

class DatabaseClient:
    """
    A client class for connecting to a PostgreSQL database and fetching data.

    This class encapsulates the connection parameters and provides a method
    to execute SQL queries, returning the results as a pandas DataFrame.
    It promotes reusability, testability, and secure handling of database
    credentials by encouraging the use of environment variables.
    """

    def __init__(self, host, port, dbname, user, password):
        """
        Initializes the DatabaseClient with database connection parameters.

        Args:
            host (str): The database host address.
            port (str or int): The database port number.
            dbname (str): The name of the database.
            user (str): The username for database access.
            password (str): The password for database access.
        """
        self.conn_params = {
            'host': host,
            'port': port,
            'dbname': dbname,
            'user': user,
            'password': password
        }

    def get_data(self, query, params=None):
        """
        Executes a SQL query and returns the results as a pandas DataFrame.

        The connection is established, the query is executed, and the connection
        is closed automatically upon completion or failure.

        Args:
            query (str): The SQL query string to be executed.
            params (tuple or list, optional): A sequence of parameters to
                                              be used with the query. These
                                              parameters are safely passed
                                              to prevent SQL injection.
                                              Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the query results.
                          Returns an empty DataFrame if no rows are fetched.

        Raises:
            psycopg.Error: If a database-specific error occurs (e.g., connection
                           failure, invalid query).
            Exception: For any other unexpected errors during execution.
        """
        df = pd.DataFrame()  # Initialize an empty DataFrame as a default return
        conn = None  # Initialize connection object to None

        try:
            # Establish a database connection using the stored parameters
            conn = psycopg.connect(**self.conn_params)
            
            # Use a context manager for the cursor to ensure it's properly closed
            # row_factory=rows.dict_row fetches results as dictionaries
            with conn.cursor(row_factory=rows.dict_row) as cur:
                print(f"Executing query:\n{query}") # Log the query being executed
                
                # Execute the query with parameters. If params is None, use an empty tuple.
                cur.execute(query, params or ())
                
                # Fetch all results and convert them into a pandas DataFrame
                df = pd.DataFrame(cur.fetchall())
                print(f"Fetched {len(df)} rows.") # Log the number of rows fetched
                
        except psycopg.Error as e:
            # Catch specific database errors and re-raise them after logging
            print(f"Database error: {e}")
            raise
        except Exception as e:
            # Catch any other unexpected errors and re-raise them after logging
            print(f"An unexpected error occurred: {e}")
            raise
        finally:
            # Ensure the database connection is closed, whether successful or not
            if conn:
                conn.close()
                print("Database connection closed.")
                
        return df
