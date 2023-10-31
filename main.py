# main.py
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session


# Dependency
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class Node(BaseModel):
    id: int
    name: str
    path: str
    children: List['Node'] = None
    properties: Dict
    created: str

    class Config:
        orm_mode = True


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

