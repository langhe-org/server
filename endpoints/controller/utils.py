from ..session_manager import SessionManager
from models.greenhouse import DbGreenhouse
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
from passlib.hash import bcrypt_sha256


def ensure_valid_greenhouse(credentials: HTTPBasicCredentials) -> DbGreenhouse:
    try:
        greenhouse_id = int(credentials.username)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    with SessionManager() as db:
        greenhouse: DbGreenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        if greenhouse and bcrypt_sha256.verify(credentials.password, greenhouse.token_hash):
            return greenhouse
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
