from .shared import app
from sqlalchemy.orm import Session
from database import engine
from models.greenhouse import DbGreenhouse, Greenhouse, CreateGreenhouse, UpdateGreenhouse


@app.get("/greenhouse/{greenhouse_id}", response_model=Greenhouse)
async def create(greenhouse_id: int):
    db = Session(engine)
    db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
    return db_greenhouse.to_greenhouse()


# TODO: restrict to admin
@app.post("/greenhouse", response_model=Greenhouse)
async def create(greenhouse: CreateGreenhouse):
    db = Session(engine)
    db_greenhouse = greenhouse.to_db_greenhouse()
    db.add(db_greenhouse)
    db.commit()
    db.refresh(db_greenhouse)
    return db_greenhouse


@app.patch("/greenhouse/{greenhouse_id}", response_model=Greenhouse)
async def update(greenhouse_id: int, greenhouse: UpdateGreenhouse):
    db = Session(engine)

    db.query(DbGreenhouse)\
       .filter(DbGreenhouse.id == greenhouse_id)\
       .update(greenhouse.__dict__)
    db.commit()

    db_greenhouse = db.query(DbGreenhouse).filter(DbGreenhouse.id == greenhouse_id).first()
    greenhouse = db_greenhouse.to_greenhouse()

    return greenhouse
