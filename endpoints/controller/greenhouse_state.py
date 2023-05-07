from ..session_manager import SessionManager
from .utils import ensure_valid_greenhouse
from models.greenhouses_state import CreateGreenhouseState
from ..shared import app
from .shared import security
from fastapi import Depends, status
from fastapi.security import HTTPBasicCredentials

@app.post("/controller/v1/greenhouse-state", status_code=status.HTTP_201_CREATED)
def create(state: CreateGreenhouseState, credentials: HTTPBasicCredentials = Depends(security)):
    greenhouse = ensure_valid_greenhouse(credentials)
    with SessionManager() as db:
        db_state = state.to_db_greenhouse_state(greenhouse.id)
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
