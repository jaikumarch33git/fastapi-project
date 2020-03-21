import asyncio
import logging
from fastapi.exceptions import HTTPException
from starlette.status import  HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from app.core.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_BUCKET
from app.core.read_file_util import FileReaderUtil
from app.core.s3_util import S3ServiceUtil
from app.db.db_client import DBClient


logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

s3ServiceUtil = S3ServiceUtil(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region=AWS_DEFAULT_REGION)
bucket = AWS_BUCKET



async def asset_upload(conn: DBClient, file: object, category: str):
    async with await conn.motor_client.start_session() as s:
        async with s.start_transaction():
            file_util = FileReaderUtil()
            temp_file_save = file_util.save_file(file)

            folder = 'assets'
            remote_storage_path = '{}/{}'.format(folder, file.filename)

            s3_upload = await s3_file_upload(storage_path=remote_storage_path, file_path=temp_file_save['path'])

            row = await conn.assets.insert_one({"url": s3_upload['url'], "source": "s3", "category": category})

            file_util.remove_file(temp_file_save['path'])

            return row.inserted_id


async def s3_file_upload(storage_path: str, file_path: str):
    with open(file_path, 'rb') as data:
        file_upload = await s3ServiceUtil.file_upload(bucket=bucket, data=data, path=storage_path)
        # file_upload = await s3ServiceUtil.presigned_post_upload(bucket=bucket, data=data, file_name= file.filename,uploadfile= file)

    if file_upload["response"]["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File Upload failed please retry after sometime",
        )

    return file_upload


async def fetch_asset_detail(conn: DBClient, search_field_value: str, search_field_name: str = '_id'):
    async with await conn.motor_client.start_session() as s:
        async with s.start_transaction():
            searched_asset = await conn.assets.find_one({search_field_name: search_field_value})

            if not searched_asset:
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Asset with id '{search_field_value}' doesn't exists in db",
                )

            return searched_asset