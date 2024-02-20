#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Resources(BaseModel, Base):
    """ """
    __tablename__ = "resources"
    link = Column(String(1024), nullable=False)
    topic_id = Column(String(60), ForeignKey('topics.id'), nullable=False)