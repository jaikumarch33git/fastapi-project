from motor.motor_asyncio import AsyncIOMotorClient
from app.db import db_client


class DataBase:
    client: db_client = None


db = DataBase()


async def get_database() -> db_client:
    return db.client
