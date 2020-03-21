import asyncio
import io
import logging

import aiobotocore
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.core.utils import request

logger = logging.getLogger(__name__)


class S3ServiceUtil:
    loop = asyncio.get_event_loop()
    awssession = aiobotocore.get_session(loop=loop)

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    # def _create_client(self):
    #     awssession = aiobotocore.get_session(loop=self.loop)
    #     client = awssession.create_client('s3', region_name='us-east-2',
    #                                       aws_secret_access_key=self.aws_secret_access_key,
    #                                       aws_access_key_id=self.aws_secret_access_key)

    # return client

    async def file_upload(self, bucket, path, data, *args, **kwargs):

        async with self.awssession.create_client('s3', region_name=self.region,
                                                 aws_secret_access_key=self.aws_secret_access_key,
                                                 aws_access_key_id=self.aws_access_key_id) as awsclient:
            file_upload_response = await awsclient.put_object(Bucket=bucket, Key=path, Body=data)

        display_response = {"response": file_upload_response}
        if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            display_response['url'] = f"https://{bucket}.s3.{self.region}.amazonaws.com/{path}"
        return display_response

    async def presigned_post_upload(self, bucket, file_name, data, uploadfile=None, *args, **kwargs):
        async with self.awssession.create_client('s3', region_name=self.region,
                                                 aws_secret_access_key=self.aws_secret_access_key,
                                                 aws_access_key_id=self.aws_access_key_id) as awsclient:
            try:
                response = awsclient.generate_presigned_post(bucket,
                                                             file_name,
                                                             Fields=None,
                                                             Conditions=None,
                                                             ExpiresIn=3600)
            except:
                HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="S3 error",
                )

            files = {'file': (file_name, data)}

            new_file = io.BytesIO(uploadfile.file.read())
            temp = {}
            temp['data'] = response['fields']
            temp['files'] = new_file

            logger.info(temp)
            http_response = await request('post', url=response['url'], data=temp)

            logger.info(http_response)
        return http_response

    async def s3_multipart_upload(self, data, loop, key, content_type, bucket):
        async with self.awssession.create_client('s3', region_name=self.region,
                                                 aws_secret_access_key=self.aws_secret_access_key,
                                                 aws_access_key_id=self.aws_access_key_id) as awsclient:
            # config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
            #                         multipart_chunksize=1024 * 25, use_threads=True)
            response = await awsclient.create_multipart_upload(Bucket=bucket, Key=key)
            upload_id = response['UploadId']

            upload_part_res = await awsclient.upload_part(Body=data, Bucket=bucket, Key=key, UploadId=upload_id,
                                                          PartNumber=1)

            multipartupload = {}
            parts = []
            part_upload = {'ETag': upload_part_res['ETag'], 'PartNumber': 1}
            parts.append(part_upload)
            multipartupload['Parts'] = parts

            complete_upload_parts = await awsclient.complete_multipart_upload(Bucket=bucket, Key=key,
                                                                              UploadId=upload_id,
                                                                              MultipartUpload=multipartupload)

            logger.info(complete_upload_parts)

            return response
