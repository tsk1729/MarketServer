from uuid import UUID

from fastapi import APIRouter, Body

from influencers import service
from influencers.models import FormData

creator_controller = APIRouter(tags=["Influencers API"])
@creator_controller.post("/creator")
def save_creator_data(data:FormData,user_id: UUID = Body()):
    return service.save_creator(data,str(user_id))

@creator_controller.get("/creator")
def get_creator_data(user_id:str):
    return service.get_creator(str(user_id))
