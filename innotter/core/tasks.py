import boto3
from django.conf import settings

from innotter.celery import app


@app.task
def upload_file_to_s3(file_path, key):
    client = boto3.client(
        "s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    client.upload_file(
        Filename=file_path,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
    )


@app.task
def send_email_to_subscribers(page, follower_list):
    ses = boto3.client("ses", settings.AWS_DEFAULT_REGION)
    ses.send_email(
        Source=settings.DEFAULT_FROM_EMAIL,
        Destination={"ToAddresses": follower_list},
        Message={
            "Subject": {"Data": f"New post on {page}.", "Charset": "utf-8"},
            "Body": {
                "Text": {"Data": f"{page} has published a new post", "Charset": "utf-8"},
            },
        },
    )

