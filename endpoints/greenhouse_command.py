from models.command import Command, ControllerCommand, CreateCommand, DbCommand
from models.greenhouses_state import DbGreenhouseState, GreenhouseState, CreateGreenhouseState
from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from fastapi import status


@app.post("/v1/greenhouse-command/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
async def something(greenhouse_id: int, command: CreateCommand):
    db = Session(engine)

    db_command = command.to_db_command(greenhouse_id)
    db.add(db_command)
    db.commit()


@app.post("/v1/greenhouse-command/{greenhouse_id}/controller-request", response_model=ControllerCommand)
async def controller_request(greenhouse_id):
    db = Session(engine)

    query_filters = db.query(DbCommand)\
       .filter(DbCommand.greenhouse_id == greenhouse_id)\
       .filter(DbCommand.processed == False)
    db_commands = query_filters.all()

    output = ControllerCommand()
    for db_command in db_commands:
        command = db_command.to_command().to_controller_command()
        if command.environment:
            if not output.environment:
                output.environment = []
            output.environment += command.environment
        if command.ipm:
            if not output.ipm:
                output.ipm = []
            output.ipm += command.ipm
        if command.lighting:
            if not output.lighting:
                output.lighting = []
            output.lighting += command.lighting
        if command.irrigation:
            if not output.irrigation:
                output.irrigation = []
            output.irrigation += command.irrigation

    query_filters.update({DbCommand.processed: True})
    db.commit()

    return output
