import motor.motor_asyncio

from app.core.config import settings


database_client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_ADDRESS)
database = database_client["SCPanel"]

applications_db = database["applications"]
foundations_db = database["foundations"]

async def insert_one(_db, data):
    return await globals()[_db].insert_one(data)


async def insert_many(_db, data):
     return await globals()[_db].insert_many(data)


async def find_one(_db, query):
    return await globals()[_db].find_one(query)


async def find(_db, query):
    cursor =  globals()[_db].find(query)
    return await cursor.to_list(length=100000000000)
    

async def update_one(_db, search_data, new_data):
    return await globals()[_db].update_one(search_data, {"$set": new_data}, upsert=True)


async def delete_one(_db, query):
    await globals()[_db].delete_one(query)