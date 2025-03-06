# database/connections.py

import psycopg2
from psycopg2 import pool

# Option A: Simple function returning a new connection each time
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname="smart_home",
#         user="postgres",
#         password="secret",
#         host="localhost",
#         port=5432
#     )
#     return conn

# Option B: Connection pool (more scalable)
# Initialize at module level (only once)
# connection_pool = pool.SimpleConnectionPool(
#     1, 10,
#     dbname="smart_home",
#     user="postgres",
#     password="secret",
#     host="localhost",
#     port=5432
# )

# def get_db_connection():
#     return connection_pool.getconn()
#
# def put_db_connection(conn):
#     connection_pool.putconn(conn)
# src/database/connections.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from mongoengine import connect

from src.models.db import db

def initialize_database(app):
    db.init_app(app)

def initialize_db():
    # Replace with your MongoDB connection string
    #mongo_uri = "mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority"

    mongo_uri = "mongodb+srv://admin:jlEpgheReUJk4Cpy@cluster0.2loew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    connect(host=mongo_uri)