import re
from typing import Optional

from pydantic import validator

from app.core.constants import EMAIL_REGEX, MOBILE_REGX
from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password


class UserBase(RWModel):
    username: str


class UserInDB(UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class UserResponse(UserBase):
    token: str


class UserLogin(RWModel):
    username: str
    password: str


class UserSignup(RWModel):
    username: str

    @validator('username')
    def is_mobile_or_email(cls, v):
        regex_name = re.compile(EMAIL_REGEX)
        email_res = regex_name.search(v)

        regex_name = re.compile(MOBILE_REGX)
        mobile_res = regex_name.search(v)

        if not email_res and not mobile_res:
            raise ValueError('Username should be valid mobile number or email id')
        return v


class UserSignupResponse(RWModel):
    username: str
    message: str


class UserVerifyOtp(RWModel):
    username: str
    otp: str
    password: str


class VerifyOTPResponse(RWModel):
    message: str


class UserUpdate(RWModel):
    username: Optional[str] = None
    password: Optional[str] = None
    image: Optional[str] = None


class RegisterUser(RWModel):
    UserName: str
    Password: str
    Email: str
    Role: str
    Phone: int
    Gender: str
