#!/usr/bin/python3
"""
Description: This file contains the definition of the BaseModel class, which provides the base functionality for all models in the application

Dependencies:
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python
- datetime: Standard datetime library for handling dates and times
- uuid: Standard library for generating universally unique identifiers (UUIDs)
- models: Custom module containing the storage instance for handling database interactions

Classes:
- BaseModel: Base class for all models, providing common attributes and methods

Attributes:
- Base: Declarative base class for SQLAlchemy models, used for creating database tables

Methods:
- __init__: Initializes a new instance of the model with provided keyword arguments
- __str__: Returns a string representation of the instance
- save: Saves the instance to the database, updating the updated_at attribute
- to_dict: Converts the instance to a dictionary representation
- delete: Deletes the instance from the database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime
from datetime import datetime
import uuid
import models
from typing import Any, Dict


Base = declarative_base()


class BaseModel():
    """
    Base class for all models, providing common attributes and methods.

    Attributes:
        id (str): The unique identifier for the instance.
        created_at (datetime): The date and time when the instance was created.
        updated_at (datetime): The date and time when the instance was last updated.
    """
    id: str = Column(String(60), nullable=False, primary_key=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a new instance of the model with provided keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments containing attribute values.

        Note:
            The created_at and updated_at attributes are automatically set to the current date and time
            if not provided in the keyword arguments. The id attribute is automatically generated if not provided.
        """
        format: str = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.strptime(value, format))
                    else:
                        setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
                self.updated_at = self.created_at
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self) -> str:
        """
        Returns a string representation of the instance.

        Returns:
            str: A string containing the class name, instance ID, and instance attributes.
        """
        cls: str = (str(type(self)).split('.')[-1]).split('\'')[0]
        return f'[{cls}] ({self.id}) {self.__dict__}'

    def save(self) -> None:
        """
        Updates the instance's updated_at attribute and saves it to storage.

        Note:
            The updated_at attribute is automatically set to the current date and time before saving.
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        models.storage.new(self)
        storage.save()

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the instance into a dictionary.

        Returns:
            dDict[str, Any]: A dictionary representation of the instance, including its attributes.
        """
        dictionary: Dict[str, Any] = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': (str(type(self)).split('.')[-1]).split('\'')[0]})

        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if ('_sa_instance_state') in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self) -> None:
        """Deletes current instance from storage"""
        from models import storage
        storage.delete(self)

