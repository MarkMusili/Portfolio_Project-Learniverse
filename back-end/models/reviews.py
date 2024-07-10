#!/usr/bin/python3
"""
File: models/review.py
Description: This file contains the definition of the Review model, which represents
             reviews provided by users in the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- Review: Model representing user reviews

Attributes:
- user_id: Foreign key referencing the User model
- text: The text content of the review

"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """
    Review model representing user reviews

    Attributes:
        user_id (str): Foreign key referencing the User model
        text (str): The text content of the review
    """
    __tablename__ = "reviews"
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    text = Column(String(1024), nullable=False)
