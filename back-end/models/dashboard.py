#!/usr/bin/python3
"""
File: models/dashboard.py
Description: This file contains the definition of the Dashboard model, which represents
             the status of roadmaps in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Dashboard: Model representing the dashboard status of roadmaps

Attributes:
- roadmap_id: Foreign key referencing the Roadmap model
- planning: Integer representing the number of roadmaps in the planning phase
- in_progress: Integer representing the number of roadmaps in progress
- completed: Integer representing the number of completed roadmaps
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Dashboard(BaseModel, Base):
    """
    Dashboard model representing the status of roadmaps

    Attributes:
        roadmap_id (str): Foreign key referencing the Roadmap model
        planning (int): Number of roadmaps in the planning phase
        in_progress (int): Number of roadmaps in progress
        completed (int): Number of completed roadmaps
    """
    __tablename__ = "dashboard"
    roadmap_id = Column(String(60), ForeignKey('roadmap.id'), nullable=False)
    planning = Column(Integer, nullable=False, default=0)
    in_progress = Column(Integer, nullable=False, default=0)
    completed = Column(Integer, nullable=False, default=0)
