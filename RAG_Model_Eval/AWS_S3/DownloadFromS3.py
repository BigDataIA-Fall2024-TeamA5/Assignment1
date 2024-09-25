import boto3
import os

# Connect to S3 using environment variables for security (recommended)
def connect_to_s3():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'your-region')  # Optional
    )

# Function to download a file from S3
def download_file_from_s3(s3_client, bucket_name, s3_file_name, local_file_name):
    try:
        # Download the file from S3 and save it locally
        with open(local_file_name, 'wb') as f:
            s3_client.download_fileobj(bucket_name, s3_file_name, f)
        print(f"File {s3_file_name} downloaded successfully to {local_file_name}")
    except Exception as e:
        print(f"Error downloading {s3_file_name}: {str(e)}")

# Function to fetch file content directly from S3 (if you don't want to save locally)
def get_file_from_s3(s3_client, bucket_name, file_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return response['Body'].read().decode('utf-8')

# Main function to run the script
def main():
    # Connect to S3
    s3 = connect_to_s3()

    # Define S3 bucket and file details
    bucket_name = 'your_bucket_name'
    s3_file_name_1 = 'your_first_file.csv'  # File 1 in S3
    s3_file_name_2 = 'your_second_file.json'  # File 2 in S3

    # Define local file paths
    local_file_name_1 = '/path/to/save/your_first_file.csv'
    local_file_name_2 = '/path/to/save/your_second_file.json'

    # Download files from S3 and save locally
    download_file_from_s3(s3, bucket_name, s3_file_name_1, local_file_name_1)
    download_file_from_s3(s3, bucket_name, s3_file_name_2, local_file_name_2)

    # Alternatively, get file content directly (without saving locally)
    file_content = get_file_from_s3(s3, bucket_name, s3_file_name_2)
    print(file_content)  # For example, to use this data directly in your app

if __name__ == "__main__":
    main()