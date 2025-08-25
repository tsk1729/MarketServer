from starlette.responses import JSONResponse
from logger import logger
from mongo import repo_manager

def get_agency(user_id):
    return repo_manager.companies.read({"_id":user_id})


def save_agency(data,user_id):
    data = data.dict()
    try:
        update = repo_manager.companies.upsert({"_id": user_id}, data)
        logger.info(f"Updated lines: Modified: {update.modified_count},Matched:{update.matched_count}")
    except Exception as e:
        logger.error(e)
    return JSONResponse(status_code=200, content={'msg': 'saved creator data'})


