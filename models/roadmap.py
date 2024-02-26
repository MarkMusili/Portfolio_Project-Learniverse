#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

class Roadmap(BaseModel, Base):
    """ """
    __tablename__ = "roadmap"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    title = Column(String(1024), nullable=False)
    introduction = Column(Text, nullable=False)
    AdditionalInfo = Column(JSON, nullable=True)
    topic = relationship('Topic', cascade='all, delete-orphan', backref='roadmap')
    dashboard = relationship('Dashboard', cascade='all, delete-orphan', backref='roadmap')

     
