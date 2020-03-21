
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse
import math
import random
import aiohttp
import datetime


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))


def generate_otp(no_of_digits):
    digits = "0123456789"
    OTP = ""

    for i in range(int(no_of_digits)):
        OTP += digits[math.floor(random.random() * 10)]
    return str(OTP)


async def request(request_type, **kwargs):
    response_dict= {}
    async with aiohttp.ClientSession() as session:
        async with getattr(session, request_type.lower())(**kwargs) as response:
            text = await response.text()
            response_dict['text'] = text
            response_dict['status_code'] = response.status
    return response_dict


def create_temp_collection():
    currtime = datetime.datetime.now().strftime("%d%m%Y%H%M%S")

    return "temp_" + currtime
