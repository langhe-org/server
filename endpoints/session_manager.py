from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from database import engine

Session = sessionmaker(engine)

@contextmanager
def SessionManager():
    try:
        session = Session()
        yield session
    finally:
        session.close()
