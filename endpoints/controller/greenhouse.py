from fastapi import Depends
from ..session_manager import SessionManager
from .utils import ensure_valid_greenhouse
from ..shared import app
from .shared import security
from models.greenhouse import DbGreenhouse, Greenhouse
from fastapi.security import HTTPBasicCredentials


@app.get("/controller/v1/greenhouse", response_model=Greenhouse)
def get(credentials: HTTPBasicCredentials = Depends(security)):
    greenhouse = ensure_valid_greenhouse(credentials)
    with SessionManager() as db:
        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse.id).first()
        return db_greenhouse.to_greenhouse()
