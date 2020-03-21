import math
import random
import requests
import logging
import json
import re

from app.core.constants import EMAIL_REGEX
from app.core.utils import request

logger = logging.getLogger(__name__)


class Msg91Util:

    msg91_send_otp_api = 'https://control.msg91.com/api/sendotp.php'
    msg91_send_otp_email_api = 'https://control.msg91.com/api/sendmailotp.php'

    def __init__(self,auth_key):
        self.auth_key = auth_key


    def generate_otp(self,no_of_digits):
        digits = "0123456789"
        OTP = ""

        for i in range(int(no_of_digits)):
            OTP += digits[math.floor(random.random() * 10)]
        return str(OTP)


    async def _send_otp_email(self,email_id,otp):
        query_params = '?otp={}&authkey={}&email={}'.format(otp, self.auth_key, email_id)
        msg91_send_otp_email_url = Msg91Util.msg91_send_otp_email_api + query_params
        # response = requests.post(msg91_send_otp_email_url)
        response = await request("post", url=msg91_send_otp_email_url)
        return response


    async def _send_otp_mobile(self,mobile_no,otp):
        otp_message = 'OTP for verification: ' + str(otp)
        query_params = '?country={}&otp={}&sender={}&message={}&mobile={}&authkey={}'.format(91,otp, 'KOBEMP', otp_message ,mobile_no,self.auth_key)
        msg91_send_otp_mobile_url = Msg91Util.msg91_send_otp_api + query_params
        # response = requests.post(msg91_send_otp_mobile_url)
        response = await request("post", url=msg91_send_otp_mobile_url)
        logger.info(response)
        return response

    async def send_otp(self,sender_address,otp):

        if re.search(EMAIL_REGEX, sender_address):
            response = await self._send_otp_email(sender_address, otp)
            return response
        else:
            response = await self._send_otp_mobile(sender_address, otp)
            return response
