#!/usr/bin/python3
"""This module instantiates an object of class based on the storage type"""
from dotenv import load_dotenv
from os import getenv

load_dotenv()

if getenv("RDMP_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.VercelDB_storage import VercelDBStorage
    storage = VercelDBStorage()

storage.reload()
