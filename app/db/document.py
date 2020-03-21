import datetime
from uuid import uuid4


class Document():

    def __init__(self, motor_client, db_name, collection_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = motor_client[db_name]
        self.collection_name = collection_name

    @staticmethod
    def _generate_id():
        return uuid4().hex

    def distinct(self, distinct_field, filter, *args, **kwargs):
        return self.db[self.collection_name].find(filter).distinct(distinct_field)

    def find_one(self, filter, *args, **kwargs):
        return self.db[self.collection_name].find_one(filter)

    def find(self, filter, *args, **kwargs):
        return self.db[self.collection_name].find(filter)

    def count(self, filter, *args, **kwargs):
        return self.db[self.collection_name].count_documents(filter)

    def aggregate(self, pipeline, *args, **kwargs):
        return self.db[self.collection_name].aggregate(pipeline)

    async def delete_one(self, filter, *args, **kwargs):
        fut = await self.db[self.collection_name].delete_one(filter)
        return fut

    async def delete_many(self, filter, *args, **kwargs):
        fut = await self.db[self.collection_name].delete_many(filter)
        return fut

    async def insert_one(self, document=None, *args, **kwargs):
        current_date = datetime.datetime.now()
        document['_id'] = self._generate_id()
        document['created_at'] = current_date
        document['updated_at'] = current_date
        fut = await self.db[self.collection_name].insert_one(document)
        return fut

    async def insert_many(self, documents, *args, **kwargs):
        current_date = datetime.datetime.now()
        for docuement in documents:
            docuement.update({'_id': self._generate_id(),
                              'created_at': current_date,
                              'updated_at': current_date})
        fut = await self.db[self.collection_name].insert_many(documents)
        return fut

    async def update_one(self, filter, update, *args, **kwargs):
        current_date = datetime.datetime.now()
        if '$set' not in update:
            update['$set'] = {}
        update['$set'].update({'updated_at': current_date})

        if '_id' in update['$set']:
            del update['$set']['_id']

        fut = await self.db[self.collection_name].update_one(filter, update)
        return fut

    async def update_many(self, filter, update, *args, **kwargs):
        current_date = datetime.datetime.now()
        if '$set' not in update:
            update['$set'] = {}
        update['$set'].update({'updated_at': current_date})
        if '_id' in update['$set']:
            del update['$set']['_id']
        fut = await self.db[self.collection_name].update_many(filter, update)
        return fut



