import boto3
import time
import urllib3
import os


# Initialize boto3 clients and environment variables
s3_client = boto3.client('s3')
bucket_name = os.getenv('BUCKET_NAME')
api_url = os.getenv('PLOTTING_API_URL')

# Debugging information
print(f"BUCKET_NAME: {bucket_name}")
print(f"PLOTTING_API_URL: {api_url}")

def lambda_handler(event, context):
    # Step 1: Create, update, delete, and recreate S3 objects with delays in between
    try:
        # Create an object in S3
        s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
        print("Object 'assignment1.txt' created with content: 'Empty Assignment 1'")
        time.sleep(2)

        # Update the object with new content
        s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
        print("Object 'assignment1.txt' updated with content: 'Empty Assignment 2222222222'")
        time.sleep(2)

        # Delete the object
        s3_client.delete_object(Bucket=bucket_name, Key='assignment1.txt')
        print("Object 'assignment1.txt' deleted.")
        time.sleep(2)

        # Recreate a new object
        s3_client.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
        print("Object 'assignment2.txt' created with content: '33'")
        time.sleep(2)

    except Exception as e:
        print(f"Error performing S3 operations: {e}")
        return {
            'statusCode': 500,
            'body': 'Error performing S3 operations.'
        }

    # Step 2: Call the plotting API if URL is provided
    if api_url:
        try:
            http = urllib3.PoolManager()
            response = http.request('POST', api_url)
            print("Plotting API invoked:", response.status)
        except Exception as e:
            print(f"Error calling plotting API: {e}")
            return {
                'statusCode': 500,
                'body': 'Error calling plotting API.'
            }
    else:
        print("Error: PLOTTING_API_URL is not set.")
        return {
            'statusCode': 400,
            'body': 'PLOTTING_API_URL is not set.'
        }

    # Return success status
    return {
        'statusCode': 200,
        'body': 'Driver Lambda executed successfully and invoked Plotting API.'
    }
