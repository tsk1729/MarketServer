from fastapi import FastAPI

from creators.controller import creator_controller

app = FastAPI()
app.include_router(creator_controller)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
