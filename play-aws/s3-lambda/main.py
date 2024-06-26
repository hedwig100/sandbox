# This script can be used as a lambda function.

import json
import boto3


def lambda_handler(event, context):
    body = json.loads(event["body"])
    return return_filename(body)


def return_filename(body):
    return_value = {"filename": body["filename"]}
    return {"statusCode": 200, "body": json.dumps(return_value)}
