from models.greenhouse import DbGreenhouse
from ..session_manager import SessionManager
from .greenhouse_state import create as create_greenhouse_state
from .utils import ensure_valid_greenhouse
from models.command import ControllerCommand, DbCommand
from models.greenhouses_state import CreateGreenhouseState
from ..shared import app
from .shared import security
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials

# @app.post("/v1/greenhouse-command/{greenhouse_id}/controller-request", response_model=ControllerCommand)
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
@app.post("/controller/v1/controller-ping", response_model=ControllerCommand)
def controller_ping(greenhouse_state: CreateGreenhouseState, credentials: HTTPBasicCredentials = Depends(security)):
    greenhouse: DbGreenhouse = ensure_valid_greenhouse(credentials)
    create_greenhouse_state(greenhouse_state, credentials=credentials)
    return controller_request(greenhouse.id)
