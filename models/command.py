from math import floor
from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from typing import List
from .db_base import Base
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from models.greenhouses_state import ControlMode, LightingRecipeIntensity, SulfurIntensity
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


# number of seconds from midnight
def time_value(t: time) -> int:
    t = datetime.combine(date.today(), t)
    midnight = datetime.combine(date.today(), time(0, 0))
    delta: timedelta = t - midnight
    return floor(delta.total_seconds())


def timedelta_value(td: timedelta) -> int:
    return floor(td.total_seconds())


class EnvironmentRecipeCommand(BaseModel):
    day_temperature: float | None
    night_temperature: float | None
    humidity_limit: float | None # should be enum (low, medium, high)?


class EnvironmentCommand(BaseModel):
    mode: ControlMode | None
    exhaust: bool | None
    heater: bool | None
    ventilator: bool | None
    recipe: EnvironmentRecipeCommand | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.exhaust is not None:
            output.append(f"exhaust " + on_off_value(self.exhaust))
        if self.heater is not None:
            output.append(f"heat " + on_off_value(self.heater))
        if self.ventilator is not None:
            output.append(f"vent " + on_off_value(self.ventilator))
        if self.recipe is not None:
            if self.recipe.day_temperature is not None:
                output.append(f"recipe day {self.recipe.day_temperature}")
            if self.recipe.night_temperature is not None:
                output.append(f"recipe night {self.recipe.night_temperature}")
            if self.recipe.humidity_limit is not None:
                output.append(f"recipe limit {self.recipe.humidity_limit}")
        return output


class IpmRecipeCommand(BaseModel):
    intensity: SulfurIntensity | None


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
    intensity: LightingRecipeIntensity | None


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
                output.append(f"recipe start {time_value(self.recipe.start_at)}")
            if self.recipe.stop_at is not None:
                output.append(f"recipe stop {time_value(self.recipe.stop_at)}")
            if self.recipe.intensity is not None:
                output.append(f"recipe intensity {self.recipe.intensity}")
        return output


class IrrigationRecipeCommand(BaseModel):
    time: time | None
    duration: timedelta | None
    sunday: bool | None
    monday: bool | None
    tuesday: bool | None
    wednesday: bool | None
    thursday: bool | None
    friday: bool | None
    saturday: bool | None


class IrrigationCommand(BaseModel):
    mode: ControlMode | None
    trigger_valve: List[bool | None] | None
    recipes: List[IrrigationRecipeCommand | None] | None

    def to_controller_command(self) -> List[str]:
        output = []
        if self.mode is not None:
            output.append(f"mode " + control_mode_value(self.mode))
        if self.trigger_valve is not None:
            for i, trigger_valve in enumerate(self.trigger_valve):
                # use one-indexing
                zone = i + 1
                if trigger_valve:
                    output.append(f"valve {i} " + on_off_value(self.trigger_valve))
        if self.recipes is not None:
            for i, recipe in enumerate(self.recipes):
                # use one-indexing
                zone = i + 1
                if recipe is not None:
                    if recipe.time is not None:
                        output.append(f"recipe {zone} time {time_value(recipe.time)}")
                    if recipe.duration is not None:
                        output.append(f"recipe {zone} duration {timedelta_value(recipe.duration)}")
                    if recipe.sunday is not None:
                        output.append(f"recipe {zone} sunday {recipe.sunday}")
                    if recipe.monday is not None:
                        output.append(f"recipe {zone} monday {recipe.monday}")
                    if recipe.tuesday is not None:
                        output.append(f"recipe {zone} tuesday {recipe.tuesday}")
                    if recipe.wednesday is not None:
                        output.append(f"recipe {zone} wednesday {recipe.wednesday}")
                    if recipe.thursday is not None:
                        output.append(f"recipe {zone} thursday {recipe.thursday}")
                    if recipe.friday is not None:
                        output.append(f"recipe {zone} friday {recipe.friday}")
                    if recipe.saturday is not None:
                        output.append(f"recipe {zone} saturday {recipe.saturday}")
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
