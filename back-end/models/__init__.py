#!/usr/bin/python3
"""This module instantiates an object of class based on the storage type"""
from dotenv import load_dotenv
from models.engine.VercelDB_storage import VercelDBStorage

load_dotenv()

storage = VercelDBStorage()
storage.reload()
