from motor.motor_asyncio import AsyncIOMotorClient
from utils.setting_manager import SETTING
from datetime import datetime

async def write_uid_db(uid: int, qq: int):
    mongo = AsyncIOMotorClient(SETTING.db_mongo.url)
    coll = mongo["commspt-bot"]["uid"]
    i = await coll.find_one({"qq": qq})

    r = {"uid": uid, "qq": qq, "last_update": datetime.now().timestamp()}

    if i:
        await coll.update_one({"qq": qq}, {"$set": r})
    else:
        await coll.insert_one(r)
    
    mongo.close()

async def get_uid(qq: int):
    mongo = AsyncIOMotorClient(SETTING.db_mongo.url)
    coll = mongo["commspt-bot"]["uid"]
    i = await coll.find_one({"qq": qq})

    if i:
        return i["uid"]
    
    mongo.close()