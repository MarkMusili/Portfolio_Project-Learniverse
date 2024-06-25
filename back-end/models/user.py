#!/usr/bin/python3
""" """
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, LargeBinary, Table, ForeignKey
from sqlalchemy.orm import relationship

user_roadmap = Table('user_roadmap', Base.metadata,
                     Column('user_id', String(60), ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                     Column('roadmap_id', String(60), ForeignKey('roadmap.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))


class User(BaseModel, Base):
    """ """
    svg_data = '''<?xml version="1.0"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="340" height="340">
    <path fill="#DDD" d="m169,.5a169,169 0 1,0 2,0zm0,86a76,76 0 1
    1-2,0zM57,287q27-35 67-35h92q40,0 67,35a164,164 0 0,1-226,0"/>
    </svg>'''
    binary_data = svg_data.encode('utf-8')
    
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    # photo = Column(LargeBinary, default=binary_data)
    reviews = relationship('Review', cascade='all, delete-orphan', backref='user')
    roadmaps = relationship("Roadmap", secondary=user_roadmap, viewonly=False, backref='user')
