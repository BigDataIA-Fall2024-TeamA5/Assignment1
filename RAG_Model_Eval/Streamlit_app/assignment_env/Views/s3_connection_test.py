import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Function to test S3 connection and fetch file
def test_s3_connection(bucket_name, file_key):
    try:
        # Attempt to fetch the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        print("Connection Successful!")

        # Check the file type by ContentType
        content_type = response['ContentType']
        print(f"Content Type: {content_type}")

        # Read the file content
        file_content = response['Body'].read()

        # If it's a text file, attempt to decode it
        if "text" in content_type or content_type == "application/json":
            file_text = file_content.decode('utf-8')
            print(f"File Content of '{file_key}':\n{file_text}")
        else:
            print(f"Binary file '{file_key}' fetched successfully. File size: {len(file_content)} bytes")

    except Exception as e:
        print(f"Error fetching file from S3: {e}")

# Set your S3 bucket name and the file key (path to the file within the bucket)
bucket_name = "ragmodelbucket-fall2024-group5"   # Replace with your bucket name
file_key = "GAIA/2023/validation/2b3ef98c-cc05-450b-a719-711aee40ac65.mp3"    # Replace with the path to the file within your bucket

# Test the S3 connection
test_s3_connection(bucket_name, file_key)