from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


class CompanyData(BaseModel):
    companyName: str
    domain: str
    pincode: str
    gmail: EmailStr
    website: Optional[str] = None
    contactPerson: str
    mobile: constr(min_length=10, max_length=15)  # allows phone validation
    address: str
    companySize: str
    budgetRangeMin: str
    budgetRangeMax: str
    industries: List[str]
    preferredPlatforms: List[str]
    description: str
