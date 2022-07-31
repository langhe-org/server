from .user import *
from .greenhouse import *
from .users_greenhouse import *
from .greenhouses_state import *
from .shared import Base
import os
from sqlalchemy import MetaData, create_engine

DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING')
engine = create_engine(DATABASE_CONNECTION_STRING, future=True)
# engine = create_engine(DATABASE_CONNECTION_STRING, echo=True, future=True)

engine.connect()
Base.metadata.create_all(engine)
