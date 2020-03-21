import logging
from datetime import timedelta

from fastapi import APIRouter, Body, Depends
from redis import StrictRedis
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from app.db import db_client
from app.db.db_client import DBClient
from app.db.redis import get_redis
from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ....core.jwt import create_access_token
from ....crud.shortcuts import check_free_username, verify_otp
from ....crud.user import execute_otp_flow, get_user_by_username, create_user, insert_user_session_token_in_db
from ....db.mongodb import  get_database
from ....models.user import UserResponse, UserSignup, UserLogin, UserResponse, UserSignupResponse, UserVerifyOtp, \
    UserBase, VerifyOTPResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/users/login", response_model=UserResponse, tags=["authentication"])
async def login(
        user: UserLogin = Body(...), db: db_client = Depends(get_database),
        redis_client: StrictRedis = Depends(get_redis)
):
    dbuser = await get_user_by_username(db, user.username)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"username": dbuser.username}, expires_delta=access_token_expires
    )

    await insert_user_session_token_in_db(redis_client,UserResponse(**dbuser.dict(), token=token))

    return UserResponse(**dbuser.dict(), token=token)


@router.post(
    "/users/signup",
    response_model=UserSignupResponse,
    tags=["authentication"],
    status_code=HTTP_202_ACCEPTED,
)
async def register(
        user: UserSignup = Body(...), db: DBClient = Depends(get_database),
        redis_client: StrictRedis = Depends(get_redis)
):
    await check_free_username(db, user.username)

    user_in_response = await execute_otp_flow(redis_client, user)
    return user_in_response


@router.post("/users/verify-otp",
    response_model=VerifyOTPResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED)
async def verify_created_user(
         user: UserVerifyOtp = Body(...), db: DBClient = Depends(get_database),
        redis_client: StrictRedis = Depends(get_redis)
):

    await verify_otp(redis_client, user)
    res = await create_user(db, user)

    redis_client.delete("CREATE_USER_" + user.username)

    return res