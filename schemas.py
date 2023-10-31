# main.py
from typing import Optional, List, Dict

from pydantic import BaseModel


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
