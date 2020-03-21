import asyncio
from email.message import EmailMessage
from aiosmtplib import send

from app.core.config import SMTP_USERNAME, SMTP_PASSWORD, SMTP_HOSTNAME, SMTP_PORT


async def send_mail(mail_to: str):
    message = EmailMessage()
    message["From"] = "jaikumarch33@gmail.com"
    message["To"] = mail_to
    message["Subject"] = "Welcome Onboard"
    message.set_content("""Hey Partner!

We are very pleased that you are joining our team.
 
""")

    await send(
        message,
        hostname=SMTP_HOSTNAME,
        port=SMTP_PORT,
        use_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD
    )


event_loop = asyncio.get_event_loop()
