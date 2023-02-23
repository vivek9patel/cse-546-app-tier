from services.aws.s3 import S3
from services.aws.sqs import SQS

class AWS:
    def __init__(self,app) -> None:
        self.app = app
        self.app.config['S3_KEY'] = "AKIARZBJ2UJJNGZDQO36"
        self.app.config['S3_SECRET'] = "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"
    
    def s3(self):
        return S3(self.app)
    
    def sqs(self):
        return SQS()