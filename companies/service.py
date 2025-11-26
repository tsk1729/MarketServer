import uuid

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


def save_post(data, user_id):
    # Accepts data as a CompanyPost model (with image_file_id, image_link)
    # Saves all fields, ensuring type consistency for Mongo
    if hasattr(data, "dict"):
        data = data.dict()
    data['postId'] = str(uuid.uuid4())
    try:
        update = repo_manager.company_posts.add_to_array_field({"_id": user_id}, "posts", data)
        logger.info(f"Updated lines: Modified: {update.modified_count},Matched:{update.matched_count}")
        return JSONResponse(status_code=200, content={'message':"Success"})
    except Exception as e:
        logger.error(e)


def get_posts(user_id):
    data = repo_manager.company_posts.read({"_id":user_id})
    return JSONResponse(status_code=200, content ={'data':data})
