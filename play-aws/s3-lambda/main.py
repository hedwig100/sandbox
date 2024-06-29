# This script can be used as a lambda function.

import json
import boto3

from http.server import BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.parse_request()


def lambda_handler(event, context):
    headers = event["headers"]

    body = json.loads(event["body"])
    return return_filename(body)


def return_filename(body):
    return_value = {"filename": body["filename"]}
    return {"statusCode": 200, "body": json.dumps(return_value)}
