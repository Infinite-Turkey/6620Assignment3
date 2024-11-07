# app.py
from aws_cdk import App
from storage_tracking_stack import StorageAndTrackingStack
from plotting_stack import PlottingLambdaStack
from api_stack import ApiGatewayStack
from driver_stack import DriverLambdaStack

app = App()

# 创建 StorageAndTrackingStack
storage_and_tracking_stack = StorageAndTrackingStack(app, "StorageAndTrackingStack")

# 创建 PlottingLambdaStack，配置 Plotting Lambda
plotting_lambda_stack = PlottingLambdaStack(app, "PlottingLambdaStack",
                                            dynamodb_table=storage_and_tracking_stack.table,
                                            s3_bucket=storage_and_tracking_stack.bucket)

# 创建 ApiGatewayStack，并将其与 Plotting Lambda 集成
api_gateway_stack = ApiGatewayStack(app, "ApiGatewayStack", plotting_lambda=plotting_lambda_stack.plotting_lambda)

# 创建 DriverLambdaStack，并传递 API URL 和 API ID
driver_lambda_stack = DriverLambdaStack(app, "DriverLambdaStack", 
                                        s3_bucket=storage_and_tracking_stack.bucket, 
                                        plotting_api_url=api_gateway_stack.api_url,
                                        plotting_api_id=api_gateway_stack.api_id)

app.synth()
