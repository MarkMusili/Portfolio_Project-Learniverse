#!/usr/bin/python3
"""
File: models/user.py
Description: This file contains the definition of the User model, which represents
             users within the application

Dependencies:
- models.basemodel: BaseModel and Base classes for database interactions
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python

Classes:
- User: Model representing users within the application
- user_roadmap: Association table for the many-to-many relationship between users and roadmaps

Attributes:
- email: User's email address
- password: User's hashed password
- first_name: User's first name
- last_name: User's last name

- session_id: Session ID for user authentication
- reset_token: Token for password reset functionality

- reviews: Relationship to the Review model
- roadmaps: Many-to-many relationship with the Roadmap model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

user_roadmap = Table('user_roadmap', Base.metadata,
                     Column('user_id', String(60), ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                     Column('roadmap_id', String(60), ForeignKey('roadmap.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))


class User(BaseModel, Base):
    """
    User model representing users within the application

    Attributes:
        email (str): User's email address
        password (str): User's hashed password
        first_name (str): User's first name
        last_name (str): User's last name

        session_id (Optional[str]): Session ID for user authentication
        reset_token (Optional[str]): Token for password reset functionality

        reviews (List[Review]): Relationship to the Review model
        roadmaps (List[Roadmap]): Many-to-many relationship with the Roadmap model
    """   
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    reviews = relationship('Review', cascade='all, delete-orphan', backref='user')
    roadmaps = relationship("Roadmap", secondary=user_roadmap, viewonly=False, backref='user')
