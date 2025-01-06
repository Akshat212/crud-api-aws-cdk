from aws_cdk import core
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_dax as dax

class ApiGatewayCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        tasks_table = dynamodb.Table(
            self, "TasksTable",
            partition_key=dynamodb.Attribute(name="taskId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # DAX Cluster
        dax_cluster = dax.CfnCluster(
            self, "DaxCluster",
            iam_role_arn="your-dax-role-arn",
            cluster_name="TasksDAX",
            node_type="dax.r5.large",
            replication_factor=1
        )

        # Lambda Functions
        create_task_lambda = lambda_.Function(
            self, "CreateTaskLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="create_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions")
        )

        get_task_lambda = lambda_.Function(
            self, "GetTaskLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="get_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions")
        )

        update_task_lambda = lambda_.Function(
            self, "UpdateTaskLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="update_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions")
        )

        delete_task_lambda = lambda_.Function(
            self, "DeleteTaskLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="delete_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions")
        )

        # API Gateway
        tasks_api = apigw.RestApi(self, "TasksApi")
        tasks_resource = tasks_api.root.add_resource("tasks")

        tasks_resource.add_method(
            "POST",
            apigw.LambdaIntegration(create_task_lambda)
        )

        task_id_resource = tasks_resource.add_resource("{taskId}")

        task_id_resource.add_method(
            "GET",
            apigw.LambdaIntegration(get_task_lambda)
        )

        task_id_resource.add_method(
            "PUT",
            apigw.LambdaIntegration(update_task_lambda)
        )

        task_id_resource.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_task_lambda)
        )