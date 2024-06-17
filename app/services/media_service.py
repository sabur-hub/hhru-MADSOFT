import io
from minio import Minio
from fastapi import UploadFile
from uuid import uuid4

minio_client = Minio(
    endpoint="minio:9000",
    access_key="minio_access",
    secret_key="minio_secret",
    secure=False
)

bucket_name = "memes"

# Create the bucket if it does not exist
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

def upload_image(file: UploadFile):
    file_id = str(uuid4())
    file_extension = file.filename.split(".")[-1]
    file_name = f"{file_id}.{file_extension}"
    content = io.BytesIO(file.file.read())
    file.file.seek(0)
    
    minio_client.put_object(
        bucket_name,
        file_name,
        content,
        length=-1,
        part_size=10*1024*1024,
        content_type=file.content_type
    )
    
    return file_name

def get_image_url(file_name: str):
    return minio_client.presigned_get_object(bucket_name, file_name)
