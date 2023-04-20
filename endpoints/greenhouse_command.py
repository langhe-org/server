from endpoints.session_manager import SessionManager
from endpoints.greenhouse_state import create as create_greenhouse_state
from models.command import Command, ControllerCommand, CreateCommand, DbCommand
from models.greenhouses_state import DbGreenhouseState, GreenhouseState, CreateGreenhouseState
from .shared import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from fastapi import status


@app.post("/v1/greenhouse-command/{greenhouse_id}", status_code=status.HTTP_201_CREATED)
def create(greenhouse_id: int, command: CreateCommand):
    with SessionManager() as db:
        db_command = command.to_db_command(greenhouse_id)
        db.add(db_command)
        db.commit()


@app.post("/v1/greenhouse-command/{greenhouse_id}/controller-request", response_model=ControllerCommand)
def controller_request(greenhouse_id):
    with SessionManager() as db:
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

# RESTless API for controller (requested by Kyle)
@app.post("/v1/controller-ping/{greenhouse_id}", response_model=ControllerCommand)
def controller_ping(greenhouse_id: int, greenhouse_state: CreateGreenhouseState):
    create_greenhouse_state(greenhouse_id, greenhouse_state)
    return controller_request(greenhouse_id)
