from fastapi import Depends, HTTPException, status
from endpoints.session_manager import SessionManager
from .shared import app, security
from .utils import ensure_valid_jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models.user import DbUser, User, UpdateUser
from models.users_greenhouse import DbUserGreenhouse
from fastapi.security import HTTPAuthorizationCredentials

@app.get("/v1/account", response_model=User)
def get(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()
        if db_user:
            user = db_user.to_user()
            greenhouses = db.query(DbUserGreenhouse).filter(DbUserGreenhouse.user_id == user.id).all()
            user.greenhouse_ids = []
            for greenhouse_id in greenhouses:
                user.greenhouse_ids.append(greenhouse_id.greenhouse_id)
            return user
        else:
            # there should be a user for each JWT
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.patch("/v1/account", response_model=User)
def update(user: UpdateUser, credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        db.query(DbUser)\
            .filter(DbUser.email == jwt["email"])\
            .update(user.__dict__)
        db.commit()

        db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()
        user = db_user.to_user()

        return user


@app.post("/v1/account/link-greenhouse/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
def link_greenhouse(greenhouse_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()

        already_exists = db.query(DbUserGreenhouse)\
            .filter(DbUserGreenhouse.user_id == db_user.id)\
            .filter(DbUserGreenhouse.greenhouse_id == greenhouse_id)\
            .scalar()
        if already_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        db.add(DbUserGreenhouse(user_id=db_user.id, greenhouse_id=greenhouse_id))
        db.commit()

@app.delete("/v1/account/link-greenhouse/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
def unlink_greenhouse(greenhouse_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        db_user = db.query(DbUser).filter(DbUser.email == jwt["email"]).first()

        relation = db.query(DbUserGreenhouse)\
            .filter(DbUserGreenhouse.user_id == db_user.id)\
            .filter(DbUserGreenhouse.greenhouse_id == greenhouse_id)\
            .scalar()

        if not relation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        db.delete(relation)
        db.commit()
