from ..session_manager import SessionManager
from models.greenhouse import DbGreenhouse
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials
# from passlib.hash import bcrypt_sha256


def ensure_valid_greenhouse(credentials: HTTPBasicCredentials, greenhouse_id: int) -> DbGreenhouse:
    ensure_valid_greenhouse(credentials, greenhouse_id)
    with SessionManager() as db:
        greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        if greenhouse:
            return greenhouse
            # bcrypt_sha256.verify("joshua", hash)
            # (greenhouse.password)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
