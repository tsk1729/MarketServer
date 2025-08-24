from pydantic import BaseModel, EmailStr
from typing import List, Optional


class FormData(BaseModel):
    name: str
    mobile: str
    gmail: EmailStr
    address: str
    pincode: str
    languages: List[str]
    chargePerPostMin: str
    chargePerPostMax: str
    instagramId: str
    youtubeLink: Optional[str] = None
    twitterLink: Optional[str] = None

