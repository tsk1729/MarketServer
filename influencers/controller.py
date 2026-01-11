from typing import Literal, Union
from uuid import UUID

from fastapi import APIRouter, Body
from pydantic import conint

from influencers import service
from influencers.models import FormData, ProofSubmission

creator_controller = APIRouter(tags=["Influencers API"])
@creator_controller.post("/creator")
def save_creator_data(data:FormData,user_id: UUID = Body()):
    return service.save_creator(data,str(user_id))

@creator_controller.get("/creator")
def get_creator_data(user_id:str):
    return service.get_creator(str(user_id))

@creator_controller.post("/creators/{influencer_id}/proofs")
def submit_proofs(influencer_id:UUID,post_id:UUID,proofs:ProofSubmission):
    return service.submit_proof(str(influencer_id),str(post_id),proofs)


from fastapi import Query
from typing import Literal
from uuid import UUID

@creator_controller.get("/brand/posts", summary="Get all brand posts")
def get_posts(
    user_id: UUID = Query(...),
    page_size: int = Query(10, ge=1, le=100),
    last_value: Union[str , None] = Query(None),
    direction: conint(strict=True) = Query(1, enum=[1, -1]),
    sort_field: str = Query("_id"),
):
    return service.get_posts(page_size, last_value, direction, sort_field)
