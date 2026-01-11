import json
from uuid import UUID
from fastapi import APIRouter, Body, UploadFile, File, Form, HTTPException
from starlette.responses import JSONResponse

from brands import service
from brands.models import CompanyData, CompanyPost, Status
from imagekit.service import upload_image_service, delete_image_service
from logger import logger
from mongo import repo_manager

company_controller = APIRouter(tags=["Brands API"])

@company_controller.post("/agency")
def save_agency(data: CompanyData, user_id: UUID = Body()):
    return service.save_agency(data, str(user_id))

@company_controller.get("/agency")
def get_agency(user_id: str):
    return service.get_agency(str(user_id))


@company_controller.post("/posts",summary= "Create brand posts")
def save_posts( data: str = Form(...),
                user_id: UUID = Form(...),
                file: UploadFile = File(...)):
    try:
        data = json.loads(data)
        post = CompanyPost(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse input data: {str(e)}")
    try:
        imgkit_resp = upload_image_service(
            file=file,
            folder=f"/agency/{user_id}",
            use_unique_file_name=True,
            is_private_file=False,
            tags=None,
        )
        post = post.model_dump()
        post["fileId"] = imgkit_resp.file_id
        post["restaurantImage"]  =imgkit_resp.url
        return service.save_post(post, str(user_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed generate url for image : {str(e)}")

# @company_controller.post("/posts")
# async def save_posts(
#     file: UploadFile = File(...),
#     companyPost: CompanyPost = Body(...)  # Expecting JSON string
#
# ):
#     """
#     Accepts multipart/form-data and handles image upload via ImageKit.
#     """
#     import json
#     try:
#         # Parse keyValuePairs from JSON string
#         # key_value_list = json.loads(keyValuePairs)
#         # Upload image to ImageKit
#         imgkit_resp = await upload_image_service(
#             file=file,
#             folder="/agency",
#             use_unique_file_name=True,
#             is_private_file=False,
#             tags=None,
#         )
#         image_file_id = imgkit_resp.get("file_id") or imgkit_resp.get("fileId")
#         image_link = imgkit_resp.get("url")
#         # post = CompanyPost(
#         #     restaurantName=restaurantName,
#         #     description=description,
#         #     itemsToPromote=itemsToPromote,
#         #     minFollowers=minFollowers,
#         #     minFollowersUnit=minFollowersUnit,
#         #     keyValuePairs=key_value_list,
#         #     googleMapsLink=googleMapsLink,
#         #     address=address,
#         #     guidelines=guidelines,
#         #     category=category,
#         #     image_file_id=image_file_id,
#         #     image_link=image_link,
#         # )
#         # return service.save_post(post, str(user_id))
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to save post: {str(e)}")

@company_controller.get("/posts",summary= "Get brand posts by brand_id")
def get_posts(user_id: UUID):
    return service.get_posts(str(user_id))


@company_controller.get("/post",summary= "Get brand post with full description")
def get_posts(user_id: UUID,post_id: UUID):
    return service.get_post(str(user_id),str(post_id))




@company_controller.get("/posts/key-value-example",summary= "Dummy example")
def example_key_value_pairs(post: CompanyPost):
    return JSONResponse(content=post.dict())

@company_controller.put("/update_post",summary= "Update brand post")
def update_post(user_id:UUID = Form(...),
                use_existing_image:bool = Form(...),
                data: str = Form(...),
                post_id: UUID = Form(...),
                file: UploadFile = File(None)):
    try:
        if use_existing_image is False and file is None:
            return JSONResponse(status_code=400, content={"msg":"File is required"})
        data = json.loads(data)
        post = CompanyPost(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse input data: {str(e)}")
    try:
        user_id = str(user_id)
        post_id = str(post_id)
        post = post.model_dump()
        if use_existing_image is False:
            imgkit_resp = upload_image_service(
                file=file,
                folder=f"/agency/{user_id}",
                use_unique_file_name=True,
                is_private_file=False,
                tags=None,
            )
            new_file_id = imgkit_resp.file_id
            post["fileId"] = new_file_id
            post["restaurantImage"] =imgkit_resp.url
            response = repo_manager.brand_posts.read({"_id":post_id})
            existing_file_id  =response["fileId"]
            try:
                delete_image_service(existing_file_id)
            except Exception as e:
                logger.debug("Failed to delete existing image")
            post["fileId"] = new_file_id
        data["postId"] = post_id
        return service.update_post(post_id,post)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed update : {str(e)}")



# @company_controller.put("/update_post")
# def update_post(user_id:UUID = Form(...),
#                 use_existing_image:bool = Form(...),
#                 data: str = Form(...),
#                 post_id: UUID = Form(...),
#                 file: UploadFile = File(None)):
#     try:
#         if use_existing_image is False and file is None:
#             return JSONResponse(status_code=400, content={"msg":"File is required"})
#         data = json.loads(data)
#         post = CompanyPost(**data)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to parse input data: {str(e)}")
#     try:
#         user_id = str(user_id)
#         post_id = str(post_id)
#         post = post.model_dump()
#         if use_existing_image is False:
#             imgkit_resp = upload_image_service(
#                 file=file,
#                 folder="/agency",
#                 use_unique_file_name=True,
#                 is_private_file=False,
#                 tags=None,
#             )
#             file_id = imgkit_resp.file_id
#             post["fileId"] = file_id
#             post["restaurantImage"] =imgkit_resp.url
#
#             # following query is a bit costly operation results the same
#             # unwind_pipe_line = [{"$match": {"_id": user_id}},
#             #              {"$unwind": "$posts"},
#             #              {"$match": {"posts.postId": post_id}},
#             #              {"$project": {"_id": 0, "fileId": 1}}]
#
#
#             pipeline = [
#                 {"$match": {"_id": user_id}},
#                 {"$project": {
#                     "_id": 0,
#                     "fileIds": {
#                         "$map": {
#                             "input": {
#                                 "$filter": {
#                                     "input": "$posts",
#                                     "as": "post",
#                                     "cond": {"$eq": ["$$post.postId", post_id]}
#                                 }
#                             },
#                             "as": "post",
#                             "in": "$$post.fileId"
#                         }
#                     }
#                 }}
#             ]
#
#             response = list(repo_manager.company_posts.collection.aggregate(pipeline))
#             existing_file_id = response[0]["fileIds"][0]
#             try:
#                 delete_image_service(existing_file_id)
#             except Exception as e:
#                 logger.debug("Failed to delete existing image")
#             post["fileId"] = file_id
#         data["postId"] = post_id
#         return service.update_post(user_id,post_id,post)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed update : {str(e)}")
#

@company_controller.post("/update_status",summary= "Update brand post status")
def pause(post_id:UUID,status: Status):
    return service.update_status(post_id,status.value)


