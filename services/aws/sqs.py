import boto3
import json
import time
import asyncio

class SQS:
    def __init__(self) -> None:
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        self.request_queue_url = "https://sqs.us-east-1.amazonaws.com/122494296658/ec3_request_queue"
        self.response_queue_url = "https://sqs.us-east-1.amazonaws.com/122494296658/ec3_response_queue"
        pass
    
    def push_to_sqs(self,name,prediction):
        body = {
            'name': name,
            'prediction': prediction
        }
        response = self.sqs.send_message(
            QueueUrl=self.response_queue_url,
            DelaySeconds=10,
            MessageBody=(
                json.dumps(body)
            )
        )
        return response


    def poll_from_sqs(self):
        messeages = self.sqs.receive_message(
            QueueUrl=self.request_queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            WaitTimeSeconds=10
        )
        if('Messages' in messeages):
            return messeages
        return []
    

    async def setIntervalPolling(self):
        while True:
            messages = self.poll_from_sqs()
            for message in messages:
                if message:
                    recepitHandle = message['ReceiptHandle']
                    message = json.loads(message['Body'])
                    # print(message)
                    fileName = message['FileName']
                    s3Entry = message['S3Entry']
                    print("New Message: ",fileName)
                    deleteMessageRes = self.sqs.delete_message(
                                    QueueUrl=self.request_queue_url,
                                    ReceiptHandle=recepitHandle)
                    print(deleteMessageRes['ResponseMetadata']['HTTPStatusCode'])
            await asyncio.sleep(5)