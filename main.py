from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.get("/world2")
async def root():
    return {"message": "Hello World2"}
