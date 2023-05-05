from ..session_manager import SessionManager
from .utils import ensure_valid_greenhouse_owner_jwt
from models.greenhouses_state import DbGreenhouseState, GreenhouseState, CreateGreenhouseState
from .shared import app, security
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials

@app.get("/client/v1/greenhouse-state/{greenhouse_id}", response_model=GreenhouseState)
def get(greenhouse_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        state = db\
            .query(DbGreenhouseState)\
            .filter(DbGreenhouseState.greenhouse_id == greenhouse_id)\
            .order_by(DbGreenhouseState.time.desc())\
            .first()
        return state.to_greenhouse_state()


@app.post("/client/v1/greenhouse-state/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
def create(greenhouse_id: int, state: CreateGreenhouseState, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        db_state = state.to_db_greenhouse_state(greenhouse_id)
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
