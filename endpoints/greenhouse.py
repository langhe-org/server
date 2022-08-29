from endpoints.session_manager import SessionManager
from .shared import app
from sqlalchemy.orm import Session
from database import engine
from models.greenhouse import DbGreenhouse, Greenhouse, CreateGreenhouse, UpdateGreenhouse


@app.get("/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
async def create(greenhouse_id: int):
    with SessionManager() as db:
        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        return db_greenhouse.to_greenhouse()


# TODO: restrict to admin
@app.post("/v1/greenhouse", response_model=Greenhouse)
async def create(greenhouse: CreateGreenhouse):
    with SessionManager() as db:
        db_greenhouse = greenhouse.to_db_greenhouse()
        db.add(db_greenhouse)
        db.commit()
        db.refresh(db_greenhouse)
        return db_greenhouse


@app.patch("/v1/greenhouse/{greenhouse_id}", response_model=Greenhouse)
async def update(greenhouse_id: int, greenhouse: UpdateGreenhouse):
    with SessionManager() as db:
        db.query(DbGreenhouse)\
            .filter(DbGreenhouse.id == greenhouse_id)\
            .update(greenhouse.__dict__)
        db.commit()

        db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
        greenhouse = db_greenhouse.to_greenhouse()

        return greenhouse
