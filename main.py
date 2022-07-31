from dotenv import load_dotenv
load_dotenv()

from endpoints.main import app
from models.main import *


@app.get("/")
async def root():
    return {"message": "Hello World"}
