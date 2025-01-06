from flask import Flask, request, jsonify
from amazondax.AmazonDaxClient import AmazonDaxClient
import boto3

app = Flask(__name__)

# Initialize DAX client
dax_client = AmazonDaxClient(endpoint_urls=["dax-cluster-endpoint"])
dynamodb = boto3.resource("dynamodb")

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    task_id = data.get("taskId")
    name = data.get("name")
    description = data.get("description")
    status = data.get("status", "pending")

    if status not in ["pending", "in-progress", "completed"]:
        return jsonify({"error": "Invalid status value"}), 400

    item = {"taskId": task_id, "name": name, "description": description, "status": status}

    table = dax_client.Table("TasksTable")  # Use DAX client
    table.put_item(Item=item)

    return jsonify({"message": "Task created", "task": item}), 201

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    table = dax_client.Table("TasksTable")  # Use DAX client
    response = table.get_item(Key={"taskId": task_id})
    if "Item" not in response:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(response["Item"]), 200

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    status = data.get("status")
    if status and status not in ["pending", "in-progress", "completed"]:
        return jsonify({"error": "Invalid status value"}), 400

    table = dax_client.Table("TasksTable")  # Use DAX client
    response = table.update_item(
        Key={"taskId": task_id},
        UpdateExpression="set #n = :n, description = :d, #s = :s",
        ExpressionAttributeNames={"#n": "name", "#s": "status"},
        ExpressionAttributeValues={":n": data["name"], ":d": data["description"], ":s": status},
        ReturnValues="UPDATED_NEW"
    )

    return jsonify({"message": "Task updated", "updated": response["Attributes"]}), 200

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    table = dax_client.Table("TasksTable")  # Use DAX client
    table.delete_item(Key={"taskId": task_id})

    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
