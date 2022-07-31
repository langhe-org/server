from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.main import engine
from models.greenhouse import Greenhouse

@app.post("/greenhouse")
async def create():
    # session = Session(engine)
    # stmt = select(User).where(User.id == user_id)
    # user = session.scalars(stmt).one()
    return {}

