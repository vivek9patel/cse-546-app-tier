import asyncio, json

from services.aws import MyAWS
from services.image_classification import image_classification as predict

AWS_CONFIG = {}
AWS_CONFIG['S3_INPUT_BUCKET'] = "cse-546-ec3-input-bucket"
AWS_CONFIG['S3_OUTPUT_BUCKET'] = "cse-546-ec3-output-bucket-2"
AWS_CONFIG['S3_LOCATION'] = 'http://cse-546-ec3-output-bucket-2.s3.amazonaws.com/'

aws = MyAWS(AWS_CONFIG)
s3 = aws.s3()
sqs = aws.sqs()

async def setIntervalPolling():
    while True:
        messages = sqs.poll_from_sqs()
        for message in messages:
            if message:
                # gets message from request sqs queue
                recepitHandle = message['ReceiptHandle']
                message = json.loads(message['Body'])
                fileName = message['FileName']
                s3Entry = message['S3Entry']
                print("New Message: ",fileName)

                # get image object from S3 bucket
                img_encoded = s3.getObject(s3Entry,"input")

                # get the image prediction
                prediction = predict(img_encoded)
                print("prediction: ",prediction)

                # store results in output s3 bucket
                try:
                    fileName = fileName.split(".")[0]
                except:
                    pass
                s3.store(fileName,'({},{})'.format(fileName,prediction),"output")

                # push results to response queue
                sqs.push_to_sqs(fileName,prediction)

                # deletes from response queue
                deleteMessageRes = sqs.sqs.delete_message(
                                QueueUrl=sqs.request_queue_url,
                                ReceiptHandle=recepitHandle)
                print("deleted: ", deleteMessageRes['ResponseMetadata']['HTTPStatusCode'])
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(setIntervalPolling())