from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr

class CompanyPostKeyValuePair(BaseModel):
    platform: str
    metric: str
    value: str
    unit: str
    reward: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "platform": "Instagram",
                "metric": "Followers",
                "value": "2500",
                "unit": "K",
                "reward": 500
            }
        }
    }


class CompanyPost(BaseModel):
    restaurantName: str
    description: str
    itemsToPromote: str
    minFollowers: str
    minFollowersUnit: str
    keyValuePairs: List[CompanyPostKeyValuePair]
    googleMapsLink: str
    address: str
    guidelines: str
    category: str = "Food"

    model_config = {
        "json_schema_extra": {
            "example": {
                "restaurantName": "The Flavor Hub",
                "description": "Promote our newly launched fusion wraps and summer beverages. Ideal for food influencers.",
                "itemsToPromote": "Mexican Wrap, Paneer Tikka Wrap, Summer Mojito",
                "minFollowers": "2500",
                "minFollowersUnit": "K",
                "keyValuePairs": [
                    {
                        "platform": "Instagram",
                        "metric": "Followers",
                        "value": "2500",
                        "unit": "K",
                        "reward": "600"
                    },
                    {
                        "platform": "Instagram",
                        "metric": "Reel Views",
                        "value": "8000",
                        "unit": "K",
                        "reward": "1000"
                    },
                    {
                        "platform": "YouTube",
                        "metric": "Subscribers",
                        "value": "3000",
                        "unit": "K",
                        "reward": "1200"
                    }
                ],
                "googleMapsLink": "https://www.google.com/maps/place/Indiranagar,+Bengaluru",
                "address": "12th Main, Indiranagar, Bengaluru, Karnataka 560038",
                "guidelines": "Post 1 reel & 2 stories. Use #FlavorHubReels and tag @flavorhubofficial. No AI-generated photos allowed.",
                "category": "Food"
            }
        }
    }


class CompanyData(BaseModel):
    companyName: str
    domain: str
    pincode: str
    gmail: EmailStr
    website: Optional[str] = None
    contactPerson: str
    mobile: constr(min_length=10, max_length=15)
    address: str
    companySize: str
    budgetRangeMin: str
    budgetRangeMax: str
    industries: List[str]
    preferredPlatforms: List[str]
