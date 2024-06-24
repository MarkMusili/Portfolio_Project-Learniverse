#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Topic(BaseModel, Base):
    """ """
    __tablename__ = "topics"
    roadmap_id = Column(String(60), ForeignKey('roadmap.id'), nullable=False)
    name = Column(String(1024), nullable=False)
    description = Column(Text, nullable=False)
    milestones = Column(Text, nullable=False)
    position = Column(Integer, nullable=False)
    resources = relationship("Resources", backref="topics", cascade="all, delete-orphan")
    objectives = relationship("Objectives", backref="topics", cascade="all, delete-orphan")
