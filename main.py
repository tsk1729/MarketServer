from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from companies.controller import company_controller
from creators.controller import creator_controller

app = FastAPI()
app.include_router(creator_controller)
app.include_router(company_controller)
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
