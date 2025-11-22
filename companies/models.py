from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr


# Nested model for keyValuePairs in CompanyPost
class CompanyPostKeyValuePair(BaseModel):
    platform: str
    metric: str
    value: str
    unit: str
    reward: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "platform": "Instagram",
                "metric": "Followers",
                "value": "2500",
                "unit": "people",
                "reward": "600"
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
    restaurantImage: str
    googleMapsLink: str
    address: str
    guidelines: str
    lastDate: str
    image: str
    category: str = "Food"

    model_config = {
        "json_schema_extra": {
            "example": {
                "restaurantName": "The Flavor Hub",
                "description": "Promote our newly launched fusion wraps and summer beverages. Ideal for food influencers.",
                "itemsToPromote": "Mexican Wrap, Paneer Tikka Wrap, Summer Mojito",
                "minFollowers": "2500",
                "minFollowersUnit": "followers",
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
                "restaurantImage": "https://picsum.photos/seed/flavorhub1/800/500",
                "googleMapsLink": "https://www.google.com/maps/place/Indiranagar,+Bengaluru",
                "address": "12th Main, Indiranagar, Bengaluru, Karnataka 560038",
                "guidelines": "Post 1 reel & 2 stories. Use #FlavorHubReels and tag @flavorhubofficial. No AI-generated photos allowed.",
                "lastDate": "2025-11-30",
                "image": "https://placehold.co/200x200/png?text=Flavor+Hub+Logo",
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
    mobile: constr(min_length=10, max_length=15)  # allows phone validation
    address: str
    companySize: str
    budgetRangeMin: str
    budgetRangeMax: str
    industries: List[str]
    preferredPlatforms: List[str]
    description: str
