from .shared import app, security
from .utils import ensure_valid_jwt
from models.user import DbUser, Units, User
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import engine
import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

@app.post("/auth/google", response_model=User)
async def get_body(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    db = Session(engine)
    return get_user_create_if_not_exist(db, jwt)


def get_user_create_if_not_exist(db: Session, jwt_user: dict) -> User:
    db_user = db.query(DbUser).filter(DbUser.email == jwt_user['email']).first()
    if not db_user:
        db_user = DbUser(name=jwt_user['name'], email=jwt_user['email'], units=Units.imperial)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user.to_user()