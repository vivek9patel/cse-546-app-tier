import boto3

class S3:
    def __init__(self,app) -> None:
        app.config['S3_BUCKET'] = "cse-546-ec3-output-bucket"
        app.config['S3_LOCATION'] = 'http://cse-546-ec3-output-bucket.s3.amazonaws.com/'

        self.bucket_name = app.config['S3_BUCKET']
        self.client = boto3.client(
                    "s3",
                    aws_access_key_id=app.config['S3_KEY'],
                    aws_secret_access_key=app.config['S3_SECRET']
                )
    
    def store(self,key: str,str_data: str) -> None:
        self.client.put_object(Bucket=self.bucket_name,Body=str.encode(str_data), Key=key)