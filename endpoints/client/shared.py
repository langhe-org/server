from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
from ..shared import app

origins = os.getenv('ORIGINS').split(" ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
