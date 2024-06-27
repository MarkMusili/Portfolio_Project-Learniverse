#!/usr/bin/python3
"""
File: models/topic.py
Description: This file contains the definition of the Topic model, which represents
             topics within a roadmap in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Topic: Model representing topics within a roadmap

Attributes:
- roadmap_id: Foreign key referencing the Roadmap model
- name: The name of the topic
- description: A detailed description of the topic
- milestones: Milestones or key points within the topic
- position: The position or order of the topic within the roadmap
- resources: Relationship to the Resources model
- objectives: Relationship to the Objectives model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Topic(BaseModel, Base):
    """
    Topic model representing topics within a roadmap

    Attributes:
        roadmap_id (str): Foreign key referencing the Roadmap model
        name (str): The name of the topic
        description (str): A detailed description of the topic
        milestones (str): Milestones or key points within the topic
        position (int): The position or order of the topic within the roadmap
        resources (List[Resources]): Relationship to the Resources model
        objectives (List[Objectives]): Relationship to the Objectives model
    """
    __tablename__ = "topics"
    roadmap_id = Column(String(60), ForeignKey('roadmap.id'), nullable=False)
    name = Column(String(1024), nullable=False)
    description = Column(Text, nullable=False)
    milestones = Column(Text, nullable=False)
    position = Column(Integer, nullable=False)
    resources = relationship("Resources", backref="topics", cascade="all, delete-orphan")
    objectives = relationship("Objectives", backref="topics", cascade="all, delete-orphan")
