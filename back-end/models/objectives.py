#!/usr/bin/python3
"""
Description: This file contains the definition of the Objectives model, which represents
             the learning objectives for topics in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Objectives: Model representing the learning objectives for topics

Attributes:
- name: The name or description of the objective
- topic_id: Foreign key referencing the Topic model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Objectives(BaseModel, Base):
    """
    Objectives model representing the learning objectives for topics

    Attributes:
        name (str): The name or description of the objective
        topic_id (str): Foreign key referencing the Topic model
    """
    __tablename__ = "objectives"
    name = Column(String(1024), nullable=False)
    topic_id = Column(String(60), ForeignKey('topics.id'), nullable=False)

