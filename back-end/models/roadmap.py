#!/usr/bin/python3
"""
File: models/roadmap.py
Description: This file contains the definition of the Roadmap model, which represents
             learning roadmaps created by users in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Roadmap: Model representing user-created learning roadmaps

Attributes:
- user_id: Foreign key referencing the User model
- title: The title of the roadmap
- introduction: The introduction or overview of the roadmap
- AdditionalInfo: Additional information in JSON format

- planning: Boolean indicating if the roadmap is in the planning phase
- in_progress: Boolean indicating if the roadmap is in progress
- completed: Boolean indicating if the roadmap is completed

- topic: Relationship to the Topic model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Roadmap(BaseModel, Base):
    """
    Roadmap model representing user-created learning roadmaps

    Attributes:
        user_id (str): Foreign key referencing the User model
        title (str): The title of the roadmap
        introduction (str): The introduction or overview of the roadmap
        AdditionalInfo (dict): Additional information in JSON format

        planning (bool): Boolean indicating if the roadmap is in the planning phase
        in_progress (bool): Boolean indicating if the roadmap is in progress
        completed (bool): Boolean indicating if the roadmap is completed

        topic (List[Topic]): Relationship to the Topic model
    """
    __tablename__ = "roadmap"
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(1024), nullable=False)
    introduction = Column(Text, nullable=False)
    AdditionalInfo = Column(JSON, nullable=True)

    planning = Column(Boolean, nullable=False, default=False)
    in_progress = Column(Boolean, nullable=False, default=False)
    completed = Column(Boolean, nullable=False, default=False)

    topic = relationship('Topic', cascade='all, delete-orphan', backref='roadmap')
