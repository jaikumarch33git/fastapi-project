import logging
from typing import Optional

from fastapi import Depends
from fastapi.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,

)

from app.db.redis import get_redis
from app.models.user import UserVerifyOtp
from .user import get_user
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


async def check_free_username(
        conn: AsyncIOMotorClient, username: Optional[str] = None):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )


async def verify_otp(conn: AsyncIOMotorClient = Depends(get_redis), user: UserVerifyOtp = None):
    redis_user_details = conn.hgetall("CREATE_USER_" + user.username)

    if not redis_user_details:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User does not exists",
        )

    if user.username and user.otp:
        if user.otp != redis_user_details["otp"]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="OTP does not match, please input correct OTP",
            )
