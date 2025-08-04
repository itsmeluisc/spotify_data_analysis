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

# Example Usage (typically in a separate main script or application entry point)
if __name__ == "__main__":
    # It's highly recommended to load credentials from environment variables
    # for security and flexibility in different environments (dev, prod).
    # Make sure these environment variables are set in your system.
    db_host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
    db_port = os.getenv('DB_PORT', '5432')      # Default to '5432' if not set
    db_name = os.getenv('DB_NAME', 'your_database') # Replace with your default DB name
    db_user = os.getenv('DB_USER', 'your_user')     # Replace with your default user
    db_password = os.getenv('DB_PASSWORD', 'your_password') # Replace with your default password

    # Create an instance of the DatabaseClient
    try:
        db_client = DatabaseClient(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        # Example 1: Fetch all data from a table
        print("\n--- Example 1: Fetching all users ---")
        users_df = db_client.get_data("SELECT id, name, email FROM users;")
        if not users_df.empty:
            print(users_df.head())
        else:
            print("No users found or table is empty.")

        # Example 2: Fetch data with parameters (recommended for security)
        print("\n--- Example 2: Fetching active products ---")
        products_df = db_client.get_data(
            "SELECT product_name, price FROM products WHERE status = %s;",
            params=('active',)
        )
        if not products_df.empty:
            print(products_df.head())
        else:
            print("No active products found.")

        # Example 3: Demonstrate error handling (e.g., table not found)
        print("\n--- Example 3: Demonstrating error handling (non-existent table) ---")
        try:
            non_existent_df = db_client.get_data("SELECT * FROM non_existent_table;")
        except psycopg.Error as e:
            print(f"Caught expected database error: {e}")
        except Exception as e:
            print(f"Caught unexpected error: {e}")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An error occurred during client initialization or example execution: {e}")