from endpoints.session_manager import SessionManager
from models.users_greenhouse import DbUserGreenhouse
from .shared import app, security
from models.user import DbPermission, DbUser, PermissionType
from fastapi import Depends, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

### returns parsed JWT
def ensure_valid_jwt(credentials: HTTPAuthorizationCredentials):
    try:
        return id_token.verify_oauth2_token(credentials.credentials, requests.Request(), GOOGLE_CLIENT_ID)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def ensure_valid_greenhouse_owner_jwt(credentials: HTTPAuthorizationCredentials, greenhouse_id: int):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        is_owner = db.query(
            DbUser, DbUserGreenhouse
        ).filter(
            DbUser.email == jwt["email"]
        ).filter(
            DbUserGreenhouse.greenhouse_id == greenhouse_id
        ).filter(
            DbUserGreenhouse.user_id == DbUser.id
        ).first() is not None
    if is_owner:
        return jwt
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def ensure_valid_admin_jwt(credentials: HTTPAuthorizationCredentials):
    jwt = ensure_valid_jwt(credentials)
    with SessionManager() as db:
        is_admin = db.query(
            DbUser, DbPermission
        ).filter(
            DbUser.email == jwt["email"]
        ).filter(
            DbPermission.user_id == DbUser.id
        ).filter(
            DbPermission.permission == PermissionType.admin
        ).first() is not None

        if is_admin:
            return jwt
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
