import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TasksTable")

    task_id = event["pathParameters"]["taskId"]
    table.delete_item(Key={"taskId": task_id})

    return {"statusCode": 200, "body": json.dumps({"message": "Task deleted"})}