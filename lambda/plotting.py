import boto3
import matplotlib.pyplot as plt
import io
import time
import datetime
import matplotlib.dates as mdates
import os

# Set MPLCONFIGDIR to /tmp to avoid matplotlib cache issues in Lambda
os.environ['MPLCONFIGDIR'] = '/tmp'

# Initialize AWS resources and environment variables
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
table_name = os.getenv('DYNAMODB_TABLE_NAME')
bucket_name = os.getenv('BUCKET_NAME')

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)

    # Get the current time and calculate the time 10 seconds ago
    now = int(time.time())  # Current timestamp as integer
    ten_seconds_ago = now - 10  # 10 seconds ago, also as integer

    # Query DynamoDB for items in the last 10 seconds
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('BucketName').eq(bucket_name) & 
                               boto3.dynamodb.conditions.Key('Timestamp').between(ten_seconds_ago, now)
    )

    # Extract the relevant data for plotting
    items = response['Items']
    timestamps = [datetime.datetime.fromtimestamp(item['Timestamp']) for item in items]
    sizes = [int(item.get('TotalSize', 0)) for item in items]  # Use 'TotalSize' as the correct field name

    # Query the maximum bucket size
    response_max = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('BucketName').eq(bucket_name),
        ProjectionExpression='TotalSize',
        Limit=1,
        ScanIndexForward=False  # Sort descending to get the largest size
    )

    max_size = int(response_max['Items'][0].get('TotalSize', 0)) if response_max['Items'] else 0

    # Plotting using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, sizes, label='Bucket Size (last 10s)', marker='o')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator())
    plt.axhline(y=max_size, color='r', linestyle='--', label=f'Max Size: {max_size} bytes')
    plt.title('Bucket Size Changes (Last 10 Seconds)')
    plt.xlabel('Time')
    plt.ylabel('Size (Bytes)')
    plt.legend()
    plt.gcf().autofmt_xdate()

    # Save plot to buffer and upload to S3
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plot_key = 'plot.png'
    s3_client.put_object(Bucket=bucket_name, Key=plot_key, Body=buf, ContentType='image/png')

    return {
        'statusCode': 200,
        'body': f"Plot successfully generated and uploaded to S3 as {plot_key}."
    }
