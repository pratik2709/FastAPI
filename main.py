# main.py
import multiprocessing

import redis as redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy import text
from sqlalchemy.orm import Session

# Dependency
from database import SessionLocal
from schemas import Item


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World1"}

@app.post("/item")
async def create_item(item: Item):
    return item

@app.get("/node")
async def getNodes(db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM construct_node_tree('Rocket')")).scalar()
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return result

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def compute(value: multiprocessing.Value):
    # Simulate some computation
    with value.get_lock():
        value.value += 1
    redis_client.set("compute_result", value)

@app.post("/compute")
async def compute(background_tasks: BackgroundTasks):
    res = multiprocessing.Value('i',1)
    m1 = multiprocessing.Process(target=compute, args=(res,))
    background_tasks.add_task(m1.start)
    return {"message": f"compute started {res.value}"}

