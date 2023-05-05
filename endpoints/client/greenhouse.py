from fastapi import Depends
from ..session_manager import SessionManager
from .utils import ensure_valid_admin_jwt, ensure_valid_greenhouse_owner_jwt
from .shared import app, security
from sqlalchemy.orm import Session
from database import engine
from models.greenhouse import DbGreenhouse, Greenhouse, CreateGreenhouse, UpdateGreenhouse
from fastapi.security import HTTPAuthorizationCredentials


@app.get("/client/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
def get(greenhouse_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        return db_greenhouse.to_greenhouse()


@app.post("/client/v1/greenhouse", response_model=Greenhouse)
def create(greenhouse: CreateGreenhouse, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_admin_jwt(credentials)
    with SessionManager() as db:
        db_greenhouse = greenhouse.to_db_greenhouse()
        db.add(db_greenhouse)
        db.commit()
        db.refresh(db_greenhouse)
        return db_greenhouse


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
