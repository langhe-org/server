from .shared import app, security
from models.user import DbUser, Units, User
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

def ensure_user_greenhouse_related(db: Session, jwt, greenhouse_id: int):
    # TODO:
    pass