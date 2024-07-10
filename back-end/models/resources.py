#!/usr/bin/python3
"""
File: models/resources.py
Description: This file contains the definition of the Resources model, which represents
             the resources associated with topics in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Resources: Model representing the resources for topics

Attributes:
- link: The URL or link to the resource
- topic_id: Foreign key referencing the Topic model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Resources(BaseModel, Base):
    """
    Resources model representing the resources for topics

    Attributes:
        link (str): The URL or link to the resource
        topic_id (str): Foreign key referencing the Topic model
    """
    __tablename__ = "resources"
    link = Column(String(1024), nullable=False)
    topic_id = Column(String(60), ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
