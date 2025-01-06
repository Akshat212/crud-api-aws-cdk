import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("TasksTable")

    task_id = event["pathParameters"]["taskId"]
    data = json.loads(event["body"])

    status = data.get("status")
    if status and status not in ["pending", "in-progress", "completed"]:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid status value"})}

    response = table.update_item(
        Key={"taskId": task_id},
        UpdateExpression="set #n = :n, description = :d, #s = :s",
        ExpressionAttributeNames={"#n": "name", "#s": "status"},
        ExpressionAttributeValues={":n": data["name"], ":d": data["description"], ":s": status},
        ReturnValues="UPDATED_NEW"
    )

    return {"statusCode": 200, "body": json.dumps({"message": "Task updated", "updated": response["Attributes"]})}