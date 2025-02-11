#/usr/bin/python3
"""
DBStorage module for handling database interactions
"""

from os import getenv
from dotenv import load_dotenv
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
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict, Union


class VercelDBStorage:
    """
    Database storage engine for handling SQLAlchemy interactions
    """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """
        Initializes a new DBStorage instance.
        
        Connects to the PostgreSQL database using environment variables.
        """
        load_dotenv()
        POSTGRES_HOST = getenv('POSTGRES_HOST')
        POSTGRES_USER = getenv('POSTGRES_USER')
        POSTGRES_DATABASE = getenv('POSTGRES_DATABASE')
        POSTGRES_PWD = getenv('POSTGRES_PASSWORD')

        self.__engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}?sslmode=require")
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def all(self, cls: str = None, user_id: str = None) -> Dict[str, Union[Review, User, Dashboard, Roadmap, Topic, Resources, Objectives]]:
        """
        Retrieves all objects from the database session.

        If a class name is specified, filters objects by that class.
        If a user id is specified, filters the object(Roadmap) with respect to that user id
        
        Args:
            cls (str, optional): The class name for filtering objects.

        Returns:
            dict: A dictionary containing objects with keys formatted as '<class_name>.<object_id>'.
        """
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)

            print(cls)
            print(user_id)
            
            if cls == "Roadmap" and user_id:
                query = self.__session.query(cls).filter(cls.user_id == user_id)
                print("user id used")
            else:
                query = self.__session.query(cls)
                print("user id not used")
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
    
    def show(self, cls: str, id: str) -> Union[Review, User, Dashboard, Roadmap, Topic, Resources, Objectives]:
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

    def fetch(self, cls_name: str, ref_id: str) -> Dict[str, Union[Review, User, Dashboard, Roadmap, Topic, Resources, Objectives]]:
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
                raise NoResultFound(f"class {cls_name} has no parent")

        return objects

    def count(self, cls: str) -> int:
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


    def new(self, obj: Union[Review, User, Dashboard, Roadmap, Topic, Resources, Objectives]) -> None:
        """
        Adds a new object to the current database session.

        Args:
            obj (object): The object to be added to the session.
        """
        self.__session.add(obj)

    def save(self) -> None:
        """
        Commits the current database session, saving any changes made to the objects.
        """
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """
        Deletes the specified object from the database session if provided.

        Args:
            obj (object, optional): The object to be deleted.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self) -> None:
        """
        Reloads the database session by recreating the session and metadata based on the engine.
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # Session = scoped_session(sec)
        # self.__session = Session()
        self.__session = scoped_session(sec)

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by specified criteria.

        Args:
            **kwargs: Arbitrary keyword arguments for querying user attributes.

        Returns:
            User: The user object matching the specified criteria.

        Raises:
            InvalidRequestError: If any of the criteria keys are invalid.
            NoResultFound: If no user matches the specified criteria.
        """
        user_keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError("Invalid user attribute")
        user = self.__session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("User not found")
        return user

    def add_user(self, first_name: str, last_name: str, email: str, password: bytes) -> User:
        """
        Create a new user.

        Args:
            first_name (str): The first name of the new user.
            last_name (str): The last name of the new user.
            email (str): The email address of the new user.
            password (bytes): The password for the new user.

        Returns:
            User: The created user object.
        """
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        self.new(new_user)
        self.save()
        return new_user
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user based on their ID.

        Args:
            user_id (str): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for updating user attributes.

        Raises:
            ValueError: If any of the criteria keys are invalid.
            NoResultFound: If no user matches the specified criteria.
        """
        user_keys = ['id', 'email', 'password', 'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise ValueError("Invalid user attribute")
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User not found")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self.save()


    def close(self) -> None:
        """
        Close working SQLAlchemy session
        """
        self.__session.close()

