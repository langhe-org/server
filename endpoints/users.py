from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.main import engine
from database.user import User

@app.get("/user/{user_id}")
async def get(user_id):
    session = Session(engine)
    stmt = select(User).where(User.id == user_id)
    user = session.scalars(stmt).one()
    return user

