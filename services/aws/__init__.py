from services.aws.s3 import S3
from services.aws.sqs import SQS

class MyAWS:
    def __init__(self,config) -> None:
        self.config = config

    def s3(self):
        return S3(self.config)
    
    def sqs(self):
        return SQS(self.config)