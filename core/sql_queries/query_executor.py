import duckdb
from utils.scripts import scipts_dict


class DuckDBQueryExecutor:
    """Executes SQL queries on a DuckDB database and saves the results to a CSV file.

    Attributes:
        connection (duckdb.DuckDBPyConnection): The connection to the DuckDB database.
    """
    def __init__(self, db_path: str):
        """Initializes the DuckDBQueryExecutor with a database connection.

        Args:
            db_path (str): The file path to the DuckDB database.

        Raises:
            Exception: If the connection to the DuckDB database fails.
        """
        self.connection = duckdb.connect(database=db_path)

    def execute_query_to_csv(self, query: str, csv_file_path: str):
        """Executes a SQL query and saves the result to a CSV file.

        Args:
            query (str): The SQL query to execute.
            csv_file_path (str): The file path where the CSV file will be saved.

        Raises:
            Exception: If there is an error executing the query or saving the result to CSV.
        """
        try:
            df = self.connection.execute(query).fetchdf()

            df.to_csv(csv_file_path, index=False)
            print(f"Query executed successfully and saved to {csv_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close_connection(self):
        """Closes the connection to the DuckDB database.

        Raises:
            Exception: If there is an error closing the connection.
        """
        self.connection.close()
        print("Connection closed.")


if __name__ == "__main__":
    db_path = "nyt_books.duckdb"
    executor = DuckDBQueryExecutor(db_path)
    for query_name in scipts_dict:
        query = scipts_dict[query_name]
        csv_path = f"core/sql_queries/results/{query_name}.csv"
        executor.execute_query_to_csv(query, csv_path)
    executor.close_connection()
