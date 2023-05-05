from ..session_manager import SessionManager
from .greenhouse_state import create as create_greenhouse_state
from .utils import ensure_valid_greenhouse_owner_jwt
from models.command import Command, ControllerCommand, CreateCommand, DbCommand
from models.greenhouses_state import DbGreenhouseState, GreenhouseState, CreateGreenhouseState
from .shared import security
from ..shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials


@app.post("/client/v1/greenhouse-command/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
def create(greenhouse_id: int, command: CreateCommand, credentials: HTTPAuthorizationCredentials = Depends(security)):
    ensure_valid_greenhouse_owner_jwt(credentials, greenhouse_id)
    with SessionManager() as db:
        db_command = command.to_db_command(greenhouse_id)
        db.add(db_command)
        db.commit()
