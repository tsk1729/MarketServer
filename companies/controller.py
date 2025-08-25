from uuid import UUID

from fastapi import APIRouter, Body

from companies import service
from companies.models import CompanyData

company_controller = APIRouter(tags=["Webhooks API"])
@company_controller.post("/agency")
def save_agency(data:CompanyData, user_id: UUID = Body()):
    return service.save_agency(data, str(user_id))

@company_controller.get("/agency")
def get_agency(user_id:str):
    return service.get_agency(str(user_id))
