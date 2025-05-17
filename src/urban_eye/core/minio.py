import boto3
from botocore.client import BaseClient
from urban_eye.settings import settings

def get_minio_client() -> BaseClient:
    client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id=settings.MINIO_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.MINIO_SECRET_ACCESS_KEY
    )
    return client
