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



