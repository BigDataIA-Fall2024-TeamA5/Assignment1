import boto3
import os
import psycopg2
import pandas as pd
from io import StringIO

# S3 connection setup
def connect_to_s3():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-2")  # Set correct region
    )

# PostgreSQL connection setup
def connect_to_postgresql():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgresqldb.cb4iuicksa3s.us-east-2.rds.amazonaws.com"),
        database=os.getenv("POSTGRES_DB", "damg7245_bigdata_group5_assignment1"),
        user=os.getenv("POSTGRES_USER", "postgresData"),
        password=os.getenv("POSTGRES_PASSWORD", "postgresql123"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

# Create table if it doesn't exist
def create_table(cursor, table_name):
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        task_id TEXT PRIMARY KEY,
        question TEXT,
        level TEXT,
        final_answer TEXT,
        file_name TEXT,
        file_path TEXT,
        annotator_metadata JSONB
    )
    ''')
import json
import numpy as np

# Clean and convert Annotator Metadata to valid JSON
def clean_annotator_metadata(metadata):
    # If metadata is a string, try to convert it to a JSON object
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            print(f"Invalid JSON format for metadata: {metadata}")
            return None  # Handle the error case as you see fit
    
    # Check for NaN or other invalid values
    for key, value in metadata.items():
        if isinstance(value, float) and np.isnan(value):
            metadata[key] = None  # Replace NaN with None
    
    return metadata

# Insert a record into the PostgreSQL table
def insert_into_postgresql(cursor, table_name, record):
    # Clean the metadata field and convert it to valid JSON
    annotator_metadata = clean_annotator_metadata(record["Annotator Metadata"])
    
    # Ensure annotator_metadata is properly formatted
    if annotator_metadata is not None:
        annotator_metadata_json = json.dumps(annotator_metadata)
    
        insert_query = f'''
        INSERT INTO {table_name} (task_id, question, level, final_answer, file_name, file_path, annotator_metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (task_id) DO NOTHING;
        '''
        cursor.execute(insert_query, (
            record["task_id"],
            record["Question"],
            record["Level"],
            record["Final answer"],
            record["file_name"],
            record["file_path"],
            annotator_metadata_json  # Insert valid JSON here
        ))
    else:
        print(f"Skipping record {record['task_id']} due to invalid metadata.")
# Load data from S3
def load_s3_file(s3, bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_data = response['Body'].read().decode('utf-8')
    return pd.read_csv(StringIO(file_data))

def main():
    # S3 and file details
    bucket_name = "ragmodelbucket-fall2024-group5"
    file1_key = "gaia_test_dataset.csv"  # First dataset file key in S3
    file2_key = "gaia_validation_dataset.csv"  # Second dataset file key in S3

    # Table names for PostgreSQL
    table1_name = "gaia_test"
    table2_name = "gaia_validation"

    # Connect to S3
    s3 = connect_to_s3()

    # Load files from S3 into DataFrames
    file1_df = load_s3_file(s3, bucket_name, file1_key)
    file2_df = load_s3_file(s3, bucket_name, file2_key)

    # Connect to PostgreSQL
    conn = connect_to_postgresql()
    cursor = conn.cursor()

    # Create tables in PostgreSQL
    create_table(cursor, table1_name)
    create_table(cursor, table2_name)

    # Insert each record from the first dataset into PostgreSQL (table 1)
    for _, record in file1_df.iterrows():
        insert_into_postgresql(cursor, table1_name, record)

    # Insert each record from the second dataset into PostgreSQL (table 2)
    for _, record in file2_df.iterrows():
        insert_into_postgresql(cursor, table2_name, record)

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Data successfully uploaded to PostgreSQL from S3.")

if __name__ == "__main__":
    main()