# database/connections.py

import psycopg2
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from mongoengine import connect

from src.models.db import db

def initialize_database(app):
    db.init_app(app)

def initialize_db():
    # Replace with your MongoDB connection string
   

    mongo_uri = ""

    connect(host=mongo_uri)
