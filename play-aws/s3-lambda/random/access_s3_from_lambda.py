import boto3

BUCKET_NAME = "***********"


class S3Client:
    def __init__(self, bucket_name: str = BUCKET_NAME) -> None:
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def get(self, key: str):
        s3_response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return s3_response["Body"]

    def put(self, key: str, object: bytes):
        return self.s3.put_object(Body=object, Bucket=self.bucket_name, Key=key)


if __name__ == "__main__":
    pass
    # client = S3Client()

    # GET
    # obj = client.get("スクリーンショット 2023-06-06 213347.png")
    # print(obj.read())

    # PUT
    # with open("README.md", mode="r") as f:
    #     obj = f.read()
    # client.put(key="sample-README.md", object=obj)
