#/usr/bin/python3
"""New storage"""
import os
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


class DBStorage:
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization"""
        load_dotenv()
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
        """"Query on the current database session all
        objects depending on class name"""
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
        """Shows a specific object"""
        if cls and id:
            if isinstance(cls, str) and isinstance(id, str):
                cls = eval(cls)
                # id = eval(id)
            query = self.__session.query(cls).filter(cls.id == id).first()
            return query

    def fetch(self, cls_name, ref_id):
        """ Fetches the children of a specific parent """
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
        """Counts the number of a certain class in the storage"""
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

