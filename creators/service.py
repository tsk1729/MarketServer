from typing import Any

from starlette.responses import JSONResponse

from logger import logger
from mongo import repo_manager


async def save_creator(data,user_id):
    data =data.dict()
    update = await repo_manager.creators.upsert({"_id":user_id},data)
    logger.info(f"Updated lines: Modified: {update.modified_count},Matched:{update.matched_count}")
    return JSONResponse(status_code=200,content={'msg':'saved creator data'})


async def get_creator(user_id):
    return await repo_manager.creators.read({"_id":user_id})
