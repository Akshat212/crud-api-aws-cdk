import boto3
from botocore.exceptions import ClientError

class Task:
    def __init__(self, task_id, name=None, description=None, is_completed=False):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.is_completed = is_completed

        #Initialize DAX client
        #self.dax_client = AmazonDaxClient(endpoint_url='url')

        #Initialize DynamoDB client
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://localhost:8000",
            region_name="fakeRegion",
            aws_access_key_id='fakeMyKeyId',       
            aws_secret_access_key='fakeSecretAccessKey'
        )
        self.table = self.dynamodb.Table('TasksTable')

    # def _get_from_cache(self):
    #     try:
    #         cached_task = self.dax_client.get_item(
    #             TableName='TasksTable',
    #             Key={'taskId': {'S': self.task_id}}
    #         )
    #         if 'Item' in cached_task:
    #             return {k: v['S'] for k, v in cached_task['Item'].items()}
    #     except ClientError as e:
    #         print(f"Error accessing DAX cache: {e}")
    #     return None
    
    # def _save_to_cache(self, task_data):
    #     try:
    #         self.dax_client.put_item(
    #             TableName='TasksTable',
    #             Item={
    #                 'taskId': {'S': self.task_id},
    #                 'name': {'S': self.name},
    #                 'description': {'S': self.description},
    #                 'is_completed': {'S': str(self.is_completed)}
    #             }
    #         )
    #     except ClientError as e:
    #         print(f"Error saving to DAX cache: {e}")
    
    def save(self):
        self.table.put_item(
            Item={
                'taskId': self.task_id,
                'name': self.name,
                'description': self.description,
                'is_completed': self.is_completed
            }
        )
        # self._save_to_cache({
        #     'taskId': self.task_id,
        #     'name': self.name,
        #     'description': self.description,
        #     'is_completed': self.is_completed
        # })

    def get(self):
        # cached_task = self._get_from_cache()
        # if cached_task:
        #     return cached_task

        response = self.table.get_item(Key={'taskId': self.task_id})
        task_data = response.get('Item', None)
        # if task_data:
        #     self._save_to_cache(task_data)
        return task_data

    def update(self):
        self.table.update_item(
            Key={'taskId': self.task_id},
            UpdateExpression="set #name = :name, description = :desc, is_completed = :completed",
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={
                ':name': self.name,
                ':desc': self.description,
                ':completed': self.is_completed
            },
        )
        # self._save_to_cache({
        #     'taskId': self.task_id,
        #     'name': self.name,
        #     'description': self.description,
        #     'is_completed': self.is_completed
        # })

    def delete(self):
        self.table.delete_item(Key={'taskId': self.task_id})
        # self.dax_client.delete_item(
        #     TableName='TasksTable',
        #     Key={'taskId': {'S': self.task_id}}
        # )