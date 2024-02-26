#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Dashboard(BaseModel, Base):
    """ """
    __tablename__ = "dashboard"
    roadmap_id = Column(String(60), ForeignKey('roadmap.id'), nullable=False)
    planning = Column(Integer, nullable=False, default=0)
    in_progress = Column(Integer, nullable=False, default=0)
    completed = Column(Integer, nullable=False, default=0)
