from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from typing import List
from .db_base import Base
from pydantic import BaseModel
from datetime import datetime, time, timedelta
from models.greenhouses_state import ControlMode
from fastapi.encoders import jsonable_encoder
import json


def on_off_value(v: bool) -> str:
    if v:
        return "on"
    else:
        return "off"

def control_mode_value(v: ControlMode) -> str:
    match v:
        case ControlMode.automatic:
            return "auto"
        case ControlMode.manual:
            return "manual"


class EnvironmentRecipeCommand(BaseModel):
    day_temperature: float | None
    night_temperature: float | None
    humidity_limit: float | None # should be enum (hight, medium, high)?


class EnvironmentCommand(BaseModel):
    mode: ControlMode | None
    exhaust: bool | None
    heat: bool | None
    vent: bool | None
    recipe: EnvironmentRecipeCommand | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.exhaust is not None:
            output.append(f"exhaust " + on_off_value(self.exhaust))
        if self.heat is not None:
            output.append(f"heat " + on_off_value(self.heat))
        if self.vent is not None:
            output.append(f"vent " + on_off_value(self.vent))
        if self.recipe is not None:
            if self.recipe.day_temperature is not None:
                output.append(f"recipe day {self.recipe.day_temperature}")
            if self.recipe.night_temperature is not None:
                output.append(f"recipe night {self.recipe.night_temperature}")
            if self.recipe.humidity_limit is not None:
                output.append(f"recipe limit {self.recipe.humidity_limit}")
        return output


class IpmRecipeCommand(BaseModel):
    intensity: int | None # should be enum (hight, medium, high)?


class IpmCommand(BaseModel):
    mode: ControlMode | None
    sulfur: bool | None
    recipe: IpmRecipeCommand | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.sulfur is not None:
            output.append(f"sulfur " + on_off_value(self.sulfur))
        if self.recipe is not None:
            if self.recipe.intensity is not None:
                output.append(f"recipe intensity {self.recipe.intensity}")
        return output


class LightingRecipeCommand(BaseModel):
    start_at: time | None
    stop_at: time | None
    intensity: int | None # should be enum (hight, medium, high)?


class LightingCommand(BaseModel):
    mode: ControlMode | None
    light: bool | None
    recipe: LightingRecipeCommand | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.light is not None:
            output.append(f"light " + on_off_value(self.light))
        if self.recipe is not None:
            if self.recipe.start_at is not None:
                output.append(f"recipe start {self.recipe.start_at}") # TODO: format the way he wants it
            if self.recipe.stop_at is not None:
                output.append(f"recipe stop {self.recipe.stop_at}") # TODO:
            if self.recipe.intensity is not None:
                output.append(f"recipe intensity {self.recipe.intensity}")
        return output


class IrrigationRecipeZoneCommand(BaseModel):
    start_window: time | None
    stop_window: time | None
    duration: timedelta | None
    frequency: timedelta | None


class IrrigationRecipeCommand(BaseModel):
    zones: List[IrrigationRecipeZoneCommand | None]


class IrrigationCommand(BaseModel):
    mode: ControlMode | None
    trigger_valve: int | None
    recipe: IrrigationRecipeCommand | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.trigger_valve is not None:
            output.append(f"valve " + on_off_value(self.trigger_valve))
        if self.recipe is not None:
            for i, zone in enumerate(self.recipe.zones): # TODO: add index to output
                if zone is not None:
                    if zone.start_window is not None:
                        output.append(f"recipe {i} start {zone.start_window}") # TODO: format
                    if zone.stop_window is not None:
                        output.append(f"recipe {i} stop {zone.stop_window}") # TODO: format
                    if zone.duration is not None:
                        output.append(f"recipe {i} duration {zone.duration}") # TODO: format
                    if zone.frequency is not None:
                        output.append(f"recipe {i} frequency {zone.frequency}") # TODO: format
        return output


class Command(BaseModel):
    id: int
    greenhouse_id: int
    time: datetime
    processed: bool
    environment: EnvironmentCommand | None
    ipm: IpmCommand | None
    lighting: LightingCommand | None
    irrigation: IrrigationCommand | None

    def to_controller_command(self):
        output = ControllerCommand()
        if self.environment is not None:
            output.environment = self.environment.to_controller_command()
        if self.ipm is not None:
            output.ipm = self.ipm.to_controller_command()
        if self.lighting is not None:
            output.lighting = self.lighting.to_controller_command()
        if self.irrigation is not None:
            output.irrigation = self.irrigation.to_controller_command()
        return output

    def to_db_command(self):
        values=dict(self)
        del values['id']
        del values['greenhouse_id']
        del values['time']
        del values['processed']
        return DbCommand(
            id=self.id,
            greenhouse_id=self.greenhouse_id,
            time=self.time,
            processed=self.processed,
            command=json.dumps(jsonable_encoder(values))
        )


class DbCommand(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    time = Column(DateTime, nullable=False, index=True, server_default=func.now())
    processed = Column(Boolean, nullable=False)
    command = Column(JSON, nullable=False)

    def __repr__(self):
        return f"Command(id={self.id!r}, greenhouse_id={self.greenhouse_id!r}, time={self.time!r}, processed={self.processed!r}, command={self.command!r}"

    def to_command(self) -> Command:
        data = json.loads(self.command)
        return Command(
            id=self.id,
            greenhouse_id=self.greenhouse_id,
            time=self.time,
            processed=self.processed,
            environment=data["environment"],
            ipm=data["ipm"],
            lighting=data["lighting"],
            irrigation=data["irrigation"],
        )


class CreateCommand(BaseModel):
    environment: EnvironmentCommand | None
    ipm: IpmCommand | None
    lighting: LightingCommand | None
    irrigation: IrrigationCommand | None

    def to_db_command(self, greenhouse_id: int) -> DbCommand:
        values=dict(self)
        return DbCommand(
            greenhouse_id=greenhouse_id,
            processed=False,
            command=json.dumps(jsonable_encoder(values))
        )


class ControllerCommand(BaseModel):
    environment: List[str] | None
    ipm: List[str] | None
    lighting: List[str] | None
    irrigation: List[str] | None