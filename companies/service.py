import uuid
from fastapi import status
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

#
# def save_post(data, user_id):
#     # Accepts data as a CompanyPost model (with image_file_id, image_link)
#     # Saves all fields, ensuring type consistency for Mongo
#     if hasattr(data, "dict"):
#         data = data.dict()
#     data['postId'] = str(uuid.uuid4())
#     data['status'] = "active"
#     try:
#         update = repo_manager.company_posts.add_to_array_field({"_id": user_id}, "posts", data)
#         logger.info(f"Updated lines: Modified: {update.modified_count},Matched:{update.matched_count}")
#         return JSONResponse(status_code=200, content={'message':"Success"})
#     except Exception as e:
#         logger.error(e)

def save_post(data, user_id):
    # Accepts data as a CompanyPost model (with image_file_id, image_link)
    # Saves all fields, ensuring type consistency for Mongo
    if hasattr(data, "dict"):
        data = data.dict()
    data['userId'] = user_id
    data['_id'] = str(uuid.uuid4())
    data['status'] = "active"
    try:
        update = repo_manager.brand_posts.create(data)
        logger.info(f"Created post {update}")
        return JSONResponse(status_code=200, content={'message':"Success"})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={'message':"Failed to create post"})

def get_posts(user_id):
    data = repo_manager.brand_posts.read_all({"userId":user_id})
    data = list(data)
    return JSONResponse(status_code=200, content ={'posts':data})


def get_post(user_id,post_id):
    data = repo_manager.brand_posts.read({"_id":post_id, "userId":user_id})
    return JSONResponse(status_code=200, content ={'data':data})

def update_post(post_id,data):
    n = repo_manager.brand_posts.upsert({'_id':post_id}, data)
    logger.info(f"Updated lines: Modified: {n},Matched:{n}")
    return JSONResponse(status_code=200, content ={'msg':'updated post'})


# def update_post(user_id,post_id,data):
#     update_fields = {f"posts.$[item].{key}":value  for key, value in data.items()}
#     n = repo_manager.company_posts.collection.update_one({"_id":user_id},
#                                                      {"$set":update_fields},
#                                                       array_filters= [{"item.postId":post_id}])
#     return JSONResponse(status_code=200, content ={'msg':'updated post'})


def update_status(post_id, status):
    post_id = str(post_id)
    n = repo_manager.brand_posts.update({"_id":post_id}, {"status":status})
    return JSONResponse(status_code=200, content ={'modified_count':n.modified_count,'matched_count':n.matched_count,'message':"Updated status successfully"})