import psycopg2
import boto3
import os
import pandas as pd
from io import StringIO

# S3 connection setup (use environment variables for safety)
def connect_to_s3():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "your-region")  # Set your AWS region here
    )

# PostgreSQL connection setup (use environment variables for safety)
def connect_to_postgresql():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "your_host"),
        database=os.getenv("POSTGRES_DB", "your_dbname"),
        user=os.getenv("POSTGRES_USER", "your_username"),
        password=os.getenv("POSTGRES_PASSWORD", "your_password"),
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

# Insert a record into the PostgreSQL table
def insert_into_postgresql(cursor, table_name, record):
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
        record["Annotator Metadata"]
    ))

# Load data from S3
def load_s3_file(s3, bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_data = response['Body'].read().decode('utf-8')
    return pd.read_csv(StringIO(file_data))

def main():
    # S3 and file details
    bucket_name = "your_bucket_name"
    file1_key = "path/to/your_first_file.csv"  # First dataset file key in S3
    file2_key = "path/to/your_second_file.csv"  # Second dataset file key in S3

    # Table names for PostgreSQL
    table1_name = "gaia_dataset_1"
    table2_name = "gaia_dataset_2"

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