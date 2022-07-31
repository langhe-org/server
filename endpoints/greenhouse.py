from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.main import engine
from database.greenhouse import Greenhouse

@app.post("/greenhouse")
async def create():
    # session = Session(engine)
    # stmt = select(User).where(User.id == user_id)
    # user = session.scalars(stmt).one()
    return {}

