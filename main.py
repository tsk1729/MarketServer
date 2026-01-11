from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from brands.controller import brand_controller
from influencers.controller import influencer_controller
from imagekit.controller import imagekit_controller

app = FastAPI()
app.include_router(influencer_controller)
app.include_router(brand_controller)
app.include_router(imagekit_controller)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
