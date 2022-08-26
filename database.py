from models.user import *
from models.greenhouse import *
from models.users_greenhouse import *
from models.greenhouses_state import *
from models.db_base import Base
import os
from sqlalchemy import create_engine
import sqlalchemy

# DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')
DATABASE_UNIX_SOCKET = os.getenv('DATABASE_UNIX_SOCKET')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')


DATABASE_CONNECTION_SOCKET = sqlalchemy.engine.url.URL.create(
    drivername="postgresql",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME,
    query={"host": DATABASE_UNIX_SOCKET},
)
engine = create_engine(
    # DATABASE_CONNECTION_STRING,
    DATABASE_CONNECTION_SOCKET,
    echo=True,
    future=True,
    pool_size=5,
    pool_recycle=1800, # 30 minutes
)


engine.connect()
