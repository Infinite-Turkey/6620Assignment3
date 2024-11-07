import boto3
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Initialize AWS resources and environment variables
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
table_name = os.getenv('DYNAMODB_TABLE_NAME')
bucket_name = os.getenv('BUCKET_NAME')

def lambda_handler(event, context):
    # Step 1: Query last 10 seconds of size history from DynamoDB
    table = dynamodb.Table(table_name)
    now = datetime.utcnow()
    ten_seconds_ago = int((now - timedelta(seconds=10)).timestamp())
    
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('BucketName').eq(bucket_name) & 
        boto3.dynamodb.conditions.Key('Timestamp').between(ten_seconds_ago, int(now.timestamp()))
    )
    size_data = response['Items']

    # Step 2: Get maximum bucket size from DynamoDB
    response = table.scan(
        ProjectionExpression='TotalSize',
        FilterExpression=boto3.dynamodb.conditions.Key('BucketName').eq(bucket_name)
    )
    max_size = max(item['TotalSize'] for item in response['Items']) if response['Items'] else 0

    # Step 3: Plot size history
    timestamps = [item['TimestampStr'] for item in size_data]
    sizes = [item['TotalSize'] for item in size_data]
    
    plt.figure()
    plt.plot(timestamps, sizes, label='Bucket Size')
    plt.axhline(y=max_size, color='r', linestyle='--', label='Max Size')
    plt.xlabel('Timestamp')
    plt.ylabel('Size (Bytes)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()       # Adjust layout to prevent label cutoff
    plt.legend()
    
    # Save plot to a temporary file
    plt.savefig('/tmp/plot.png')

    # Step 4: Upload the plot to S3
    with open('/tmp/plot.png', 'rb') as f:
        s3_client.put_object(Bucket=bucket_name, Key='plot.png', Body=f)

    return {
        'statusCode': 200,
        'body': 'Plotting Lambda executed successfully, plot uploaded to S3.'
    }
