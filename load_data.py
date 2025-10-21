import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


def load_massive_csv(csv_file_path, schema_name,  table_name, columns=None):
    """
    Loads a massive CSV file into a PostgreSQL table using cursor.copy_expert().

    :param db_conn_params: Dictionary of PostgreSQL connection parameters.
    :param csv_file_path: Path to the local CSV file.
    :param table_name: The name of the table to insert data into.
    :param columns: Optional, a tuple or list of column names in the correct order 
                    if you need to specify them (e.g., if the CSV order differs).
    """
    conn = None
    cursor = None
    try:
        # 1. Connect to the database
        conn = psycopg2.connect(dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASS"],
                                host=os.environ["DB_HOST"],
                                port=os.environ["DB_PORT"])
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
            print(f"Schema '{schema_name}' created or already exists.")
        except psycopg2.Error as e:
            print(f"Error creating schema: {e}")

        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    id SERIAL PRIMARY KEY,
                    author VARCHAR(255) NOT NULL,
                    quote TEXT
                );
            """)
            print(
                f"Table '{schema_name}.{table_name}' created or already exists.")
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
        full_table_name = f'"{schema_name}"."{table_name}"'
        # 2. Open the CSV file
        print(f"Opening CSV file: {csv_file_path}")
        with open(csv_file_path, 'r') as f:
            # 3. Construct the COPY command (use STDIN for file-like object streaming)
            # Use 'CSV HEADER' to automatically skip the first row (assuming it's a header)

            if columns:
                columns_list = ', '.join(columns)
                copy_sql = f"COPY {full_table_name} ({columns_list}) FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER ',')"
            else:
                # Assumes the CSV columns are in the same order as the table columns
                copy_sql = f"COPY {full_table_name} FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER ',')"

            print(f"Executing COPY command: {copy_sql}")

            # 4. Execute the bulk copy operation
            # The file object 'f' is streamed directly to the database.
            cursor.copy_expert(copy_sql, f)

        # 5. Commit the transaction
        conn.commit()
        print("Data loaded successfully.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while loading data: {error}")
        if conn:
            conn.rollback()  # Rollback the transaction on error
    finally:
        # 6. Close the connection
        if conn and cursor:
            cursor.close()
            conn.close()
            print("PostgreSQL connection closed.")


CSV_PATH = './quotes.csv'
TABLE_NAME = 'quotes'
SCHEMA_NAME = 'quotes'

# If your table columns are 'id', 'name', 'value' and that's the CSV order:
# load_massive_csv(DB_PARAMS, CSV_PATH, TABLE_NAME)

# If you need to specify the columns:
load_massive_csv(CSV_PATH, SCHEMA_NAME, TABLE_NAME,
                 columns=['Author', 'Quote'])

# NOTE: Replace the example parameters with your actual connection details, file path, and table name.
