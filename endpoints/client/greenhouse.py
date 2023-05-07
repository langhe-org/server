from fastapi import Depends, HTTPException, status
from models.user import DbUser

from models.users_greenhouse import DbUserGreenhouse
from ..session_manager import SessionManager
from .utils import ensure_valid_jwt, ensure_valid_greenhouse_owner_jwt
from .shared import app, security
from sqlalchemy.orm import Session
from database import engine
from models.greenhouse import DbGreenhouse, Greenhouse, CreateGreenhouse, CreateGreenhouseResponse, UpdateGreenhouse
from fastapi.security import HTTPAuthorizationCredentials
from passlib.hash import bcrypt_sha256
import string
import secrets


TOKEN_LENGTH = 80


@app.get("/client/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
def get(greenhouse_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        return db_greenhouse.to_greenhouse()


@app.post("/client/v1/greenhouse", response_model=CreateGreenhouseResponse)
def create(greenhouse: CreateGreenhouse, credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        db_user: DbUser = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()
        if db_user:
            db_greenhouse = greenhouse.to_db_greenhouse()
            token = generate_token()
            db_greenhouse.token_hash = bcrypt_sha256.hash(token)
            db.add(db_greenhouse)
            db.commit()
            db.refresh(db_greenhouse)
            db.add(DbUserGreenhouse(user_id=db_user.id, greenhouse_id=db_greenhouse.id))
            db.commit()
            return CreateGreenhouseResponse(
                greenhouse=db_greenhouse.to_greenhouse(),
                token=token
            )
        else:
            # there should be a user for each JWT
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.patch("/client/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
def update(greenhouse_id: int, greenhouse: UpdateGreenhouse, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        db.query(DbGreenhouse)\
            .filter(DbGreenhouse.id == greenhouse_id)\
            .update(dict(greenhouse))
        db.commit()

        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        greenhouse = db_greenhouse.to_greenhouse()

        return greenhouse


def generate_token() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(TOKEN_LENGTH))
