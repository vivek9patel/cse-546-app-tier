import boto3

class S3:
    def __init__(self,config) -> None:
        self.config = config

        self.input_bucket = self.config['S3_INPUT_BUCKET']
        self.output_bucket = self.config['S3_OUTPUT_BUCKET']
        self.client = boto3.client(
                    "s3",
                    aws_access_key_id=self.config['S3_KEY'],
                    aws_secret_access_key=self.config['S3_SECRET']
                )
    
    def store(self,key: str,str_data: str,bucket) -> None:
        bucket_name = None
        if(bucket == "input"):
            bucket_name = self.input_bucket
        else: bucket_name = self.output_bucket
        self.client.put_object(Bucket=bucket_name,Body=str.encode(str_data), Key=key)
    
    def getObject(self,key,bucket) -> str:
        bucket_name = None
        if(bucket == "input"):
            bucket_name = self.input_bucket
        else: bucket_name = self.output_bucket
        obj = self.client.get_object(Bucket=bucket_name, Key=key)
        return obj['Body'].read()