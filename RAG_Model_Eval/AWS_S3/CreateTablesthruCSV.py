import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection setup (using environment variables from .env)
def connect_to_postgresql():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

# Create table if it doesn't exist
def create_table(cursor, table_name, columns):
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns}
    );
    '''
    cursor.execute(create_table_query)

# Dynamically generate the column definitions from the DataFrame
def get_column_definitions(df):
    # Wrap column names with spaces in double quotes and define as TEXT
    return ', '.join([f'"{col}" TEXT' if ' ' in col else f'{col} TEXT' for col in df.columns])

# Insert data into PostgreSQL table
def insert_data_to_postgresql(cursor, table_name, dataframe):
    columns = ', '.join([f'"{col}"' if ' ' in col else col for col in dataframe.columns])
    placeholders = ', '.join(['%s'] * len(dataframe.columns))
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    
    # Insert each row from the dataframe
    for row in dataframe.itertuples(index=False, name=None):
        cursor.execute(insert_query, row)

def main():
    # File paths for the two CSV files
    csv_file_1 = '/Users/aniketpatole/Documents/GitHub/New/Projects/BigData/Assignment1/RAG_Model_Eval/AWS_S3/gaia_test_dataset.csv'
    csv_file_2 = '/Users/aniketpatole/Documents/GitHub/New/Projects/BigData/Assignment1/RAG_Model_Eval/AWS_S3/gaia_validation_dataset.csv'

    # Table names for PostgreSQL
    table_name_1 = 'GAIA_Test'
    table_name_2 = 'GAIA_Validation'

    # Load CSV files into pandas DataFrames
    df1 = pd.read_csv(csv_file_1)
    df2 = pd.read_csv(csv_file_2)

    # Connect to PostgreSQL
    conn = connect_to_postgresql()
    cursor = conn.cursor()

    # Create tables based on the CSV columns
    create_table(cursor, table_name_1, get_column_definitions(df1))
    create_table(cursor, table_name_2, get_column_definitions(df2))

    # Insert data into PostgreSQL tables
    insert_data_to_postgresql(cursor, table_name_1, df1)
    insert_data_to_postgresql(cursor, table_name_2, df2)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_1} and {csv_file_2} successfully loaded into PostgreSQL.")

if __name__ == "__main__":
    main()