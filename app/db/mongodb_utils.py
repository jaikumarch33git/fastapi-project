import logging
import asyncio

from app.db.db_client import DBClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_to_mongo():
    logging.info("Connect to the database...")
    loop = asyncio.get_event_loop()
    db.client = DBClient(str(MONGODB_URL), maxPoolSize=MAX_CONNECTIONS_COUNT, minPoolSize=MIN_CONNECTIONS_COUNT, io_loop=loop)
    logging.info("Connected to the database successfully !")


async def close_mongo_connection():
    logging.info("Close the database connection...")
    db.client.close()
    logging.info("Database connection is closed！")
