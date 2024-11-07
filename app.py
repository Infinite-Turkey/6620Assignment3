from aws_cdk import App
from storage_tracking_stack import StorageAndTrackingStack
from plotting_stack import PlottingLambdaStack
from api_stack import ApiGatewayStack
from driver_stack import DriverLambdaStack

app = App()

# Create StorageAndTrackingStack to set up S3 and DynamoDB resources with Size Tracking Lambda
storage_and_tracking_stack = StorageAndTrackingStack(app, "StorageAndTrackingStack")

# Create PlottingLambdaStack, setting up the Plotting Lambda function
plotting_lambda_stack = PlottingLambdaStack(app, "PlottingLambdaStack",
                                            dynamodb_table=storage_and_tracking_stack.table,
                                            s3_bucket=storage_and_tracking_stack.bucket)

# Create ApiGatewayStack and integrate it with the Plotting Lambda function
api_gateway_stack = ApiGatewayStack(app, "ApiGatewayStack", plotting_lambda=plotting_lambda_stack.plotting_lambda)

# Create DriverLambdaStack and pass in the API URL and API ID for invocation
driver_lambda_stack = DriverLambdaStack(app, "DriverLambdaStack", 
                                        s3_bucket=storage_and_tracking_stack.bucket, 
                                        plotting_api_url=api_gateway_stack.api_url,
                                        plotting_api_id=api_gateway_stack.api_id)

app.synth()
