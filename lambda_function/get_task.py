import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TasksTable")

    task_id = event["pathParameters"]["taskId"]
    response = table.get_item(Key={"taskId": task_id})

    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}

    return {"statusCode": 200, "body": json.dumps(response["Item"])}