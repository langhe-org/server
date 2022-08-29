from endpoints.session_manager import SessionManager
from models.users_greenhouse import DbUserGreenhouse
from .shared import app, security
from .utils import ensure_valid_jwt
from models.user import DbUser, Units, User
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import engine
import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

@app.post("/v1/auth/google", response_model=User)
async def get_body(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        user = get_user_create_if_not_exist(db, jwt)
        greenhouses = db.query(DbUserGreenhouse).filter(DbUserGreenhouse.user_id == user.id).all()
        user.greenhouse_ids = []
        for greenhouse_id in greenhouses:
            user.greenhouse_ids.append(greenhouse_id.greenhouse_id)
        return user


def get_user_create_if_not_exist(db: Session, jwt_user: dict) -> User:
    db_user = db.query(DbUser).filter(DbUser.email == jwt_user['email']).first()
    if not db_user:
        db_user = DbUser(name=jwt_user['name'], email=jwt_user['email'], units=Units.imperial)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user.to_user()
