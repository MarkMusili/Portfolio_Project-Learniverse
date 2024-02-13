#!/usr/bin/python3
"""New storage"""
import os
from models.basemodel import Base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization"""
        self.__engine = create_engine(
                                    'mysql+mysqldb://{}:{}@{}:3306/{}'.
                                    format(
                                            os.getenv('HBNB_MYSQL_USER'),
                                            os.getenv('HBNB_MYSQL_PWD'),
                                            os.getenv('HBNB_MYSQL_HOST'),
                                            os.getenv('HBNB_MYSQL_DB'),
                                            # pool_pre_ping=True
                                            )
                                    )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

            self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                            expire_on_commit=False))

    def all(self, cls=None):
        """"Query on the current database session all
        objects depending on class name"""
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            classes = []
            for element in classes:
                query = self.__session.query(element)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Creates a new object"""
        self.__session.add(obj)

    def save(self):
        """Saves an object"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads an object """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """Close working SQLAlchemy session"""
        self.__session.close()
