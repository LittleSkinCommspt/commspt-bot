from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def m():
    mongo  = AsyncIOMotorClient('mongodb://root:Fg7cW8vy6GRA@0-3.mongodbservers.serinanya.5050net:27017')

    uid_coll = mongo['commspt-bot']['uid']

    i =await uid_coll.find_one({"uid": 153101})

    # i["last_update"] = datetime.now().timestamp()
    # await uid_coll.update_one({"uid": 15301}, {'$set': i})

asyncio.run(m())