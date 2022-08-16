from fastapi import Depends
from .shared import app, security
from .utils import ensure_valid_jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models.user import DbUser, User, UpdateUser
from fastapi.security import HTTPAuthorizationCredentials

@app.get("/account", response_model=User)
async def get(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    db = Session(engine)
    db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()
    return db_user.to_user()


@app.patch("/account", response_model=User)
async def update(user: UpdateUser, credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    db = Session(engine)

    db.query(DbUser)\
       .filter(DbUser.email == jwt["email"])\
       .update(user.__dict__)
    db.commit()

    db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()
    user = db_user.to_user()

    return user
