from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models.user import DbUser, User, UpdateUser

@app.get("/user/{user_id}", response_model=User)
async def get(user_id):
    db = Session(engine)
    db_user = db.query(DbUser).filter(DbUser.id == user_id).first()
    return db_user.to_user()


# TODO: user_id should come from auth
@app.patch("/user/{user_id}", response_model=User)
async def update(user_id: int, user: UpdateUser):
    db = Session(engine)

    db.query(DbUser)\
       .filter(DbUser.id == user_id)\
       .update(user.__dict__)
    db.commit()

    db_user = db.query(DbUser).filter(DbUser.id == user_id).first()
    user = db_user.to_user()

    return user
