import psycopg2
import pandas as pd
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection setup
def connect_to_postgresql():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

# Clean and validate JSON field
def clean_annotator_metadata(metadata):
    try:
        # Replace single quotes with double quotes and load as JSON
        cleaned_metadata = metadata.replace("'", "\"")
        # Parse and return the valid JSON
        return json.loads(cleaned_metadata)
    except Exception as e:
        # If it can't be parsed, return an empty JSON or None
        return None

# Insert a record into the PostgreSQL table
def insert_into_postgresql(cursor, table_name, record):
    annotator_metadata = clean_annotator_metadata(record['Annotator Metadata'])

    # Convert the cleaned dictionary to a JSON string
    if annotator_metadata:
        annotator_metadata = json.dumps(annotator_metadata)

    insert_query = f'''
    INSERT INTO {table_name} (task_id, question, level, final_answer, file_name, file_path, annotator_metadata)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (task_id) DO NOTHING;
    '''
    cursor.execute(insert_query, (
        record['task_id'],
        record['Question'],
        record['Level'],
        record['Final answer'],
        record['file_name'],
        record['file_path'],
        annotator_metadata
    ))

# Load CSV data and insert into PostgreSQL
def load_data_from_csv(file_path, table_name):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Print column names for debugging
    print("Columns in CSV file:", df.columns)

    # Connect to PostgreSQL
    conn = connect_to_postgresql()
    cursor = conn.cursor()

    # Insert each row from the CSV file into the PostgreSQL table
    for _, record in df.iterrows():
        insert_into_postgresql(cursor, table_name, record)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print(f"Data from {file_path} successfully loaded into {table_name}.")

if __name__ == "__main__":
    # Paths to your CSV files
    gaia_validation_csv_path = os.path.join(os.path.dirname(__file__), "gaia_validation_dataset.csv")
    gaia_test_csv_path = os.path.join(os.path.dirname(__file__), "gaia_test_dataset.csv")

    # Load data into gaia_validation table
    load_data_from_csv(gaia_validation_csv_path, "gaia_validation")

    # Load data into gaia_test table
    load_data_from_csv(gaia_test_csv_path, "gaia_test")