from fastapi import Depends
from ..session_manager import SessionManager
from .utils import ensure_valid_greenhouse
from ..shared import app
from .shared import security
from models.greenhouse import DbGreenhouse, Greenhouse
from fastapi.security import HTTPBasicCredentials


@app.get("/controller/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
def get(greenhouse_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    ensure_valid_greenhouse(credentials, greenhouse_id)
    with SessionManager() as db:
        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        return db_greenhouse.to_greenhouse()
