from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import (MONGO_DB)
from app.db.document import Document


class DBClient:

    def __init__(self, *args, **kwargs):
        self.motor_client = AsyncIOMotorClient(*args, **kwargs)

    def __getitem__(self, item):
        return Document(self.motor_client, MONGO_DB, item)

    def __setitem__(self,  item):
        return Document(self.motor_client, MONGO_DB, item)

    def __getattr__(self, item):
        return Document(self.motor_client, MONGO_DB, item)

    def close(self):
        self.motor_client.close()