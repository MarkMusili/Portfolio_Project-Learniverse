#!/usr/bin/python3
""" """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime
from datetime import datetime
import uuid
import models


Base = declarative_base()


class BaseModel():
    """ """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ """
        format = '%Y-%m-%dT%H:%M:%S.%f'
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

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: A string containing the class name, instance ID, and instance attributes.
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return f'[{cls}] ({self.id}) {self.__dict__}'

    def save(self):
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

    def to_dict(self):
        """
        Converts the instance into a dictionary.

        Returns:
            dict: A dictionary representation of the instance, including its attributes.
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # if ('_sa_instance_state') in dictionary.keys():
        #     del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes current instance from storage"""
        from models import storage
        storage.delete(self)

