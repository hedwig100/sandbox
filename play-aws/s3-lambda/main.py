# This script can be used as a lambda function.
from requests_toolbelt.multipart import decoder
import json
import boto3
from email.message import EmailMessage


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


def parse_multipart(headers, body):
    content_length = int(headers["Content-Length"])
    multipart_decoder = decoder.MultipartDecoder(
        body.read(content_length), headers["Content-Type"]
    )
    return multipart_decoder.parts


def filename_from_multipart_header(multipart_header):
    msg = EmailMessage()
    msg["Content-Disposition"] = multipart_header[b"Content-Disposition"]
    params = msg["Content-Disposition"].params
    return params["filename"]


### Lambda function


def lambda_upload(event, context):
    headers = event["headers"]
    body = event["body"]
    multiparts = parse_multipart(headers, body)
    filename = filename_from_multipart_header(multipart_header=multiparts[0])
    client.put(filename, multiparts[0].content)
    return {"statusCode": 200}


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
