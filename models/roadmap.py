#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy.orm import relationship

class Roadmap(BaseModel, Base):
    """ """
    __tablename__ = "roadmap"
    dashboard = relationship('Dashboard', cascade='all, delete-orphan', backref='roadmap')
     