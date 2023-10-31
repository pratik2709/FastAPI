from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from utils import Timestamp


class Node(Base, Timestamp):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String, unique=True,index=True)
    parent_id = Column(Integer, ForeignKey('node.id'), nullable=True)
    parent = relationship('Node', remote_side=[id], backref=backref('children', lazy=True))
    properties = Column(JSONB)
