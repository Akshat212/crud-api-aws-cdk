import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TasksTable")

    data = json.loads(event["body"])
    task_id = data.get("taskId")
    name = data.get("name")
    description = data.get("description")
    status = data.get("status", "pending")

    if status not in ["pending", "in-progress", "completed"]:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid status value"})}

    item = {"taskId": task_id, "name": name, "description": description, "status": status}
    table.put_item(Item=item)

    return {"statusCode": 201, "body": json.dumps({"message": "Task created", "task": item})}