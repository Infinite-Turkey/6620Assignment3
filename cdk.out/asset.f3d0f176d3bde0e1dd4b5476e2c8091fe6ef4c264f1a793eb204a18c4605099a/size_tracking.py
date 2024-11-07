import boto3
from datetime import datetime
import os

# Initialize clients and get environment variables
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bucket_name = os.environ['BUCKET_NAME']
table_name = os.environ['DYNAMODB_TABLE_NAME']

def lambda_handler(event, context):
    # Step 1: Calculate the total size and object count of the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    total_size = 0
    object_count = 0

    if 'Contents' in response:
        object_count = len(response['Contents'])
        total_size = sum(obj['Size'] for obj in response['Contents'])

    # Step 2: Prepare data to write to DynamoDB
    table = dynamodb.Table(table_name)
    timestamp = int(datetime.utcnow().timestamp())
    timestamp_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Step 3: Write the data to DynamoDB
    table.put_item(
        Item={
            'BucketName': bucket_name,
            'Timestamp': timestamp,
            'TimestampStr': timestamp_str,
            'TotalSize': total_size,
            'ObjectCount': object_count
        }
    )

    # Return the status
    return {
        'statusCode': 200,
        'body': 'Size tracking Lambda executed successfully.'
    }
