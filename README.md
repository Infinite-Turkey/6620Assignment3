# 6620Assignment3
This repository contains the code for Assignment 3 of the Cloud Computing course. The project focuses on creating and deploying AWS Lambda functions, 
managing AWS resources such as S3 buckets and DynamoDB tables, and using AWS CDK (Cloud Development Kit) for infrastructure as code.

## Project Structure
### 1.Lambda funtions:
driver.py: The main Lambda function (Driver Lambda) which orchestrates interactions between other resources.
plotting.py: Lambda function (Plotting Lambda) that generates a plot based on data in DynamoDB and stores it in S3.
size_tracking.py: Lambda function (Size Tracking Lambda) that monitors and logs changes in S3 bucket size to DynamoDB.
### 2.Stacks:
plotting_stack.py:sets up the Plotting Lambda.
api_stack.py: sets up an API Gateway for invoking the Plotting Lambda.
driver_stack.py:sets up the Driver Lambda and integrates it with the Plotting API.
storage_and_tracking_stack.py: integrates S3 and DynamoDB resources with Size Tracking Lambda.
### 3.app.py:
entry point for the AWS CDK application. It initializes and deploys all the stacks required for this assignment, organizing the resources into logical components. 
Each stack corresponds to a specific AWS service or functionality, and app.py manages their dependencies and deployment order

## Setup and Deployment
### 1.Deploy the CDK Stacks:
cdk deploy --all
### 2.Test the funtions:
go to DriverLambdaStack-DriverLambda11B3F668-bvLGb7bvbmyY lambda function, and click on "test"
### 3.Check the result:
go to bucket "storageandtrackingstack-assignment3bucketd3e8c3b4-npeb0e5agvfo", and check the "plot.png"


