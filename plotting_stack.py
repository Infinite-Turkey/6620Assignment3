# plotting_lambda_stack.py
from aws_cdk import Stack, Duration
from aws_cdk.aws_lambda import Function, Runtime, Code, Architecture
from aws_cdk.aws_dynamodb import Table
from aws_cdk.aws_s3 import Bucket
from constructs import Construct

class PlottingLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, dynamodb_table: Table, s3_bucket: Bucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.plotting_lambda = Function(
            self, "PlottingLambda",
            runtime=Runtime.PYTHON_3_8,
            handler="plotting.lambda_handler",  
            timeout=Duration.seconds(300),
            code=Code.from_asset("lambda"), 
            architecture=Architecture.ARM_64,
            environment={
                'DYNAMODB_TABLE_NAME': dynamodb_table.table_name,
                'BUCKET_NAME': s3_bucket.bucket_name
            }
        )

        s3_bucket.grant_read_write(self.plotting_lambda)
        dynamodb_table.grant_read_write_data(self.plotting_lambda)