from models.user import *
from models.greenhouse import *
from models.users_greenhouse import *
from models.greenhouses_state import *
from models.db_base import Base
import os
from sqlalchemy import create_engine

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')
# engine = create_engine(DATABASE_CONNECTION_STRING, future=True)
engine = create_engine(DATABASE_CONNECTION_STRING, echo=True, future=True)

engine.connect()
Base.metadata.create_all(engine)
