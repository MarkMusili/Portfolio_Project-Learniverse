#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Resources(BaseModel, Base):
    """ """
    __tablename__ = "resources"
    link = Column(String(1024), nullable=False)
<<<<<<< HEAD
    topic_id = Column(String(60), ForeignKey('topics.id'), nullable=False)
=======
    topic_id = Column(String(60), ForeignKey('topics.id'), nullable=False)
>>>>>>> ed5af42f6c310a68448afb9ac57fa2e99ec8e882
