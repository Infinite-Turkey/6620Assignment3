from aws_cdk import Stack,CfnOutput
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration
from aws_cdk.aws_lambda import Function
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, id: str, plotting_lambda: Function, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create REST API
        api = RestApi(self, "PlottingApi",
            rest_api_name="Plotting Service",
            description="API Gateway to trigger the Plotting Lambda."
        )

        # Create the route to Plotting Lambda
        plot_resource = api.root.add_resource("plot")
        plot_integration = LambdaIntegration(plotting_lambda)
        plot_resource.add_method("POST", plot_integration)  

        # 输出完整的 API Gateway URL 和 API ID
        self.api_url = f"{api.url}plot"
        self.api_id = api.rest_api_id

        # 导出 API ID，以便在其他 Stack 中使用
        CfnOutput(self, "PlottingApiId", value=self.api_id)