from datetime import timedelta
from fastapi import HTTPException
from redis import StrictRedis
from app.core.msg_91_util import Msg91Util
from app.core.utils import generate_otp
from app.db import db_client
from app.db.db_client import DBClient

from ..core.config import database_name, ACCESS_TOKEN_EXPIRE_MINUTES,MSG91_API_KEY
from ..models.user import UserSignup, UserInDB, UserUpdate, UserSignupResponse, UserResponse, \
    VerifyOTPResponse, UserVerifyOtp


async def get_user(conn: DBClient, username: str) -> UserInDB:
    row = await conn.user.find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_username(db: db_client, username: str) -> UserInDB:
    row = await db.user.find_one({"username": username})
    if row:
        return UserInDB(**row)


async def execute_otp_flow(conn: StrictRedis, user: UserSignup) -> UserSignupResponse:
    otp = generate_otp(6)

    conn.hmset("CREATE_USER_" + user.username,
               {'username': user.username, 'otp': otp, 'otp_counter': 20})

    conn.pexpire("CREATE_USER_" + user.username, timedelta(days=3))

    msg91_util = Msg91Util(MSG91_API_KEY)
    try:
        res = await msg91_util.send_otp(user.username, otp)
    except Exception as e:
        raise HTTPException(detail={'message': 'There was error in sending otp'}, status_code=400)

    if res['status_code'] == 200:
        return UserSignupResponse(username=user.username, message="OTP sent successfully")
    else:
        raise Exception({'message': 'There was error in sending otp'})


async def create_user(conn: DBClient, user: UserVerifyOtp) -> VerifyOTPResponse:
    user_dict = UserInDB(**user.dict())
    user_dict.change_password(user.password)

    async with await conn.motor_client.start_session() as s:
        async with s.start_transaction():
            row = await conn.user.insert_one(user_dict.dict())
            return VerifyOTPResponse(message="User verified successfully")


async def insert_user_session_token_in_db(conn: StrictRedis, user: UserResponse):
    conn.hmset(user.token,
               {'username': user.username, 'token': user.token})

    conn.pexpire(user.token, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
