from typing import Literal, Union, Optional, Dict, Any
from uuid import UUID

from dns.e164 import query
from fastapi import APIRouter, Body
from pydantic import conint

from influencers import service
from influencers.models import FormData, ProofSubmission

influencer_controller = APIRouter(tags=["Influencers API"])
@influencer_controller.post("/creator")
def save_creator_data(data:FormData,user_id: UUID = Body()):
    return service.save_creator(data,str(user_id))

@influencer_controller.get("/creator")
def get_creator_data(user_id:str):
    return service.get_creator(str(user_id))

@influencer_controller.post("/influencer/{influencer_id}/proofs", summary="influencer Submit proof to brand")
def submit_proofs(influencer_id:UUID,post_id:UUID,proofs:ProofSubmission):
    return service.submit_proof(str(influencer_id),str(post_id),proofs)


from fastapi import Query
from typing import Literal
from uuid import UUID

@influencer_controller.get("/brand/posts", summary="Get all brand posts")
def get_posts(
    user_id: UUID = Query(...),
    page_size: int = Query(10, ge=1, le=100),
    last_value: Union[str , None] = Query(None),
    direction: conint(strict=True) = Query(1, enum=[1, -1]),
    sort_field: str = Query("_id"),
):
    return service.get_posts(page_size, last_value, direction, sort_field)

@influencer_controller.post("/brands/{influencer_id}/brand-subscriptions", summary="api for influencer to subsribe to brand post")
def subscribe_to_brand(influencer_id: UUID, post_id: UUID):
    return service.subscribe_to_brand(str(influencer_id),str(post_id))


@influencer_controller.post("/brand/posts/rewards", summary="Get all brand posts")
def get_posts_by_reward( user_id: UUID = Query(...),
    page_size: int = Query(10, ge=1, le=100),
    last_cursor: Optional[Dict[str, Any]] = None,
    direction: conint(strict=True) = Query(1, enum=[1, -1]),
    ):
    return service.paginate_by_reward(page_size=page_size,last_cursor=last_cursor,direction=direction)


@influencer_controller.get(
    "/brands/{influencer_id}/brand-subscriptions/{post_id}",summary="Get status whether influencer subscribed to brand post"
)
def is_influencer_subscribed(influencer_id: UUID, post_id: UUID):
    return service.is_influencer_subscribed(str(influencer_id), str(post_id))
