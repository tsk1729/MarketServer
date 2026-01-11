from pydantic import BaseModel, EmailStr, HttpUrl
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

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Akash Mehra",
                "mobile": "9876543210",
                "gmail": "akash@example.com",
                "address": "22, Sunshine Ave, Mumbai",
                "pincode": "400001",
                "languages": ["English", "Hindi", "Marathi"],
                "chargePerPostMin": "2000",
                "chargePerPostMax": "3500",
                "instagramId": "influencer.akash",
                "youtubeLink": "https://youtube.com/user/akashmehra",
                "twitterLink": "https://twitter.com/akashmehra"
            }
        }
    }

class ProofSubmission(BaseModel):
    description: str
    link: HttpUrl

    class Config:
        json_encoders = {
            HttpUrl: str
        }