import json
from uuid import UUID
from fastapi import APIRouter, Body, UploadFile, File, Form, HTTPException
from starlette.responses import JSONResponse

from companies import service
from companies.models import CompanyData, CompanyPost
from imagekit.service import upload_image_service

company_controller = APIRouter(tags=["Webhooks API"])

@company_controller.post("/agency")
def save_agency(data: CompanyData, user_id: UUID = Body()):
    return service.save_agency(data, str(user_id))

@company_controller.get("/agency")
def get_agency(user_id: str):
    return service.get_agency(str(user_id))


@company_controller.post("/posts")
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
            folder="/agency",
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

@company_controller.get("/posts")
def get_posts(user_id: UUID):
    return service.get_posts(str(user_id))


@company_controller.get("/post")
def get_posts(user_id: UUID,post_id: UUID):
    return service.get_post(str(user_id),str(post_id))




@company_controller.get("/posts/key-value-example")
def example_key_value_pairs(post: CompanyPost):
    return JSONResponse(content=post.dict())

