from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from src.service.cloud import Cloud


class StorageRouter(APIRouter):

    """Storage Router"""

    def __init__(self):
        super().__init__()
        self.cloud = Cloud()
        self.prefix = "/storage"
        self.tags = ["Storage"]


app = StorageRouter()


@app.get("/buckets")
async def list_buckets_endpoint()-> list:
    
    """
    Summary: List all buckets
    """
    
    response = app.cloud.s3.list_buckets()
    return response.get("Buckets", [])


@app.get("/buckets/{bucket}")
async def list_bucket_endpoint(bucket: str)-> list:
    
    """
    Summary: List all objects in a bucket
    Args:
        bucket: Bucket name
    """
    response = app.cloud.s3.list_objects_v2(Bucket=bucket)
    return response.get("Contents", [])


@app.post("/objects/{bucket}")
async def upload_file_endpoint(bucket: str, key: str, file: UploadFile = File(...))-> str:

    """
    Summary: Uploads a file to a determined bucket
    Args:
        bucket: Bucket name
        key: File prefix + name
        file: File to upload
    """

    app.cloud.s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=file.file,
        ACL="public-read",
        ContentType=file.content_type,
    )
    return app.cloud.s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )


@app.get("/objects/{bucket}/{key}")
async def download_file_endpoint(bucket: str, key: str)-> FileResponse:
    """
    Summary: Downloads a file from a determined bucket
    Args:
        bucket: Bucket name
        key: File prefix + name
    """
    response = app.cloud.s3.get_object(Bucket=bucket, Key=key)
    return FileResponse(
        response["Body"],
        media_type=response["ContentType"],
        filename=response["Key"],
    )

@app.delete("/objects/{bucket}/{key}")
async def delete_file_endpoint(bucket: str, key: str)-> JSONResponse:
    """
    Summary: Deletes a file from a determined bucket
    Args:
        bucket: Bucket name
        key: File prefix + name
    """
    app.cloud.s3.delete_object(Bucket=bucket, Key=key)
    return JSONResponse(content={"message": "File deleted"}, status_code=status.HTTP_200_OK)

@app.get("/objects/{bucket}/{key}/presigned")
async def get_presigned_url_endpoint(bucket: str, key: str)-> str:
    """Generates a presigned url"""
    return app.cloud.s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )


@app.get("/objects/stream/{bucket}/{key}")
async def stream_file_endpoint(bucket: str, key: str):
    """
    Summary: Streams a file from a determined bucket
    Args:
        bucket: Bucket name
        key: File prefix + name
    """
    response = app.cloud.s3.get_object(Bucket=bucket, Key=key)
    return StreamingResponse(
        response["Body"],
        media_type=response["ContentType"],
        headers={"Content-Disposition": f"attachment; filename={response['Key']}"},
    )