#/usr/bin/python3
"""New storage"""
import os
from models.basemodel import Base
from models.reviews import Review
from models.dashboard import Dashboard
from models.user import User
from models.roadmap import Roadmap
from models.topics import Topic
from models.resources import Resources
from models.objectives import Objectives
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new DBStorage instance.
        
        Connects to the MySQL database using environment variables.
        Drops existing tables if the environment is set to test.
        """
        self.__engine = create_engine(
                                    'mysql+mysqldb://{}:{}@{}:3306/{}'.
                                    format(
                                            os.getenv('RDMP_MYSQL_USER'),
                                            os.getenv('RDMP_MYSQL_PWD'),
                                            os.getenv('RDMP_MYSQL_HOST'),
                                            os.getenv('RDMP_MYSQL_DB'),
                                            # pool_pre_ping=True
                                            )
                                    )
        if os.getenv('RDMP_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

            self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                            expire_on_commit=False))

    def all(self, cls=None):
        """
        Retrieves all objects from the database session.

        If a class name is specified, filters objects by that class.
        
        Args:
            cls (str, optional): The class name for filtering objects.

        Returns:
            dict: A dictionary containing objects with keys formatted as '<class_name>.<object_id>'.
        """
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            classes = [Review, User, Dashboard, Roadmap, Topic, Resources, Objectives]
            for element in classes:
                query = self.__session.query(element)
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj

        return objects
    
    def show(self, cls, id):
        """
        Retrieves a specific object from the database.

        Args:
            cls (str): The class name of the object.
            id (str): The ID of the object to retrieve.

        Returns:
            object: The specified object from the database.
        """
        if cls and id:
            if isinstance(cls, str) and isinstance(id, str):
                cls = eval(cls)
                # id = eval(id)
            query = self.__session.query(cls).filter(cls.id == id).first()
            return query

    def fetch(self, cls_name, ref_id):
        """
        Fetches the children of a specific parent object.

        Args:
            cls_name (str): The class name of the parent object.
            ref_id (int): The reference ID of the parent object.

        Returns:
            dict: A dictionary containing children objects with keys formatted as '<class_name>.<object_id>'.
        """
        objects = {}
        if cls_name and ref_id:
            class_map = {
                "Topic": Topic,
                "Dashboard": Dashboard,
                "Roadmap": Roadmap,
                "Review": Review,
                "Objectives": Objectives,
                "Resources": Resources
            }

            cls = class_map.get(cls_name)
            if cls is None:
                return {"error": f"Class {cls_name} not found"}

            search = ""
            if cls_name in ["Topic", "Dashboard"]:
                search = "roadmap_id"
            elif cls_name in ["Roadmap", "Review"]:
                search = "user_id"
            elif cls_name in ["Objectives", "Resources"]:
                search = "topic_id"

            if search:
                query = self.__session.query(cls).filter(getattr(cls, search) == ref_id)
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj
            else:
                return {f"** Class {cls_name} has no parent **"}

        return objects

    def count(self, cls):
        """
        Counts the number of objects of a certain class in the storage.

        Args:
            cls (str): The class name of the objects to be counted.

        Returns:
            int: The count of objects of the specified class.
        """
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        return len(objects)


    def new(self, obj):
        """
        Adds a new object to the current database session.

        Args:
            obj (object): The object to be added to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits the current database session, saving any changes made to the objects.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes the specified object from the database session if provided.

        Args:
            obj (object, optional): The object to be deleted.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database session by recreating the session and metadata based on the engine.
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """
        Close working SQLAlchemy session
        """
        self.__session.close()

