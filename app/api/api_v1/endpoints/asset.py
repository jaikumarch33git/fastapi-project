import logging
import asyncio

from fastapi import APIRouter, Body, Depends, Path, File, UploadFile, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from app.crud.asset import s3_file_upload, asset_upload,fetch_asset_detail
from app.db.db_client import DBClient
from app.db.mongodb import get_database

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()
router = APIRouter()


@router.post("/configuration/asset/file/upload", tags=["asset"], status_code=HTTP_201_CREATED)
async def upload_assets(file: UploadFile = File(...), db: DBClient = Depends(get_database),
                        category: str = Query(..., min_length=1)):

    file_upload = await asset_upload(conn=db, file=file, category=category)

    return file_upload


@router.get("/configuration/asset/file/upload", tags=["asset"], status_code=HTTP_200_OK)
async def fetch_uploaded_asset(db: DBClient = Depends(get_database), asset_id: str = Query(..., min_length=1)):
    asset_detail = await fetch_asset_detail(conn=db, search_field_value=asset_id)

    return asset_detail
