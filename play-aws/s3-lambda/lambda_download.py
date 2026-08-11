# This script can be used as a lambda function.
import json
import boto3


class S3Client:
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def get(self, key: str):
        s3_response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return s3_response["Body"]

    def put(self, key: str, object: bytes):
        return self.s3.put_object(Body=object, Bucket=self.bucket_name, Key=key)


client = S3Client()


### Lambda function

def lambda_download(event, context):
    """
    body: {
      "filename": "xxx.py"
    }
    """
    body = json.load(event["body"])
    filename = body["filename"]

    object = client.get(filename)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f"attachmentl; filename={filename}",
        },
        "body": object,
    }
