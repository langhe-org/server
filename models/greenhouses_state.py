from argparse import Action
from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, DateTime, String, Enum, func
from sqlalchemy.dialects.postgresql import JSON
from typing import List, Generic, TypeVar
import enum
from .db_base import Base
from pydantic import BaseModel
from datetime import datetime
from pydantic.generics import GenericModel


class ControlMode(enum.Enum):
    automatic = "automatic"
    manual = "manual"


class EnvironmentState(enum.Enum):
    default = "default"


class IpmState(enum.Enum):
    default = "default"


class IrrigationState(enum.Enum):
    default = "default"


class LightningState(enum.Enum):
    default = "default"


class Sensor(BaseModel):
    temperature: float = None
    humidity: float = None
    quantum : float = None

StateT = TypeVar('StateT')
class Subsystem(GenericModel,  Generic[StateT]):
    mode: ControlMode
    state: StateT


class Control(BaseModel):
    environment: Subsystem[EnvironmentState]
    ipm: Subsystem[IpmState]
    lighting: Subsystem[LightningState]
    irrigation: Subsystem[IrrigationState]


class Actuator(BaseModel):
    heater: bool
    exhaust: bool
    ventilator: bool
    sulfur: bool
    lights: bool
    valves: List[bool]


class WeatherCurrent(BaseModel):
    temperature: float
    humidity: float
    sky: str


class Weather(BaseModel):
    current: WeatherCurrent


class GreenhouseState(BaseModel):
    id: int
    greenhouse_id: int
    time: datetime
    sensor: Sensor = None
    control: Control
    actuator: Actuator
    weather: Weather = None

    class Config:
        orm_mode = True

    def to_db_greenhouse_state(self): # can the return type be strongly typed?
        return DbGreenhouseState(
            id=self.id,
            greenhouse_id=self.greenhouse_id,
            time=self.time,
            temperature=self.sensor.temperature,
            humidity=self.sensor.humidity,
            quantum=self.sensor.quantum,
            environment_mode=self.control.environment.mode,
            environment_state=self.control.environment.state,
            ipm_mode=self.control.ipm.mode,
            ipm_state=self.control.ipm.state,
            lighting_mode=self.control.lighting.mode,
            lighting_state=self.control.lighting.state,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_state=self.control.irrigation.state,
            heater=self.actuator.heater,
            exhaust=self.actuator.exhaust,
            ventilator=self.actuator.ventilator,
            sulfur=self.actuator.sulfur,
            lights=self.actuator.lights,
            valves=self.actuator.valves,
            weather_temperature=self.weather.current.temperature,
            weather_humidity=self.weather.current.humidity,
            weather_sky=self.weather.current.sky,
        )


class DbGreenhouseState(Base):
    __tablename__ = "greenhouse_state"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    time = Column(DateTime, nullable=False, index=True, server_default=func.now())
    temperature = Column(Integer, nullable=False)
    humidity = Column(Float, nullable=False)
    quantum = Column(Float, nullable=False)
    environment_mode = Column(Enum(ControlMode), nullable=False)
    environment_state = Column(Enum(EnvironmentState), nullable=False)
    ipm_mode = Column(Enum(ControlMode), nullable=False)
    ipm_state = Column(Enum(IpmState), nullable=False)
    lighting_mode = Column(Enum(ControlMode), nullable=False)
    lighting_state = Column(Enum(LightningState), nullable=False)
    irrigation_mode = Column(Enum(ControlMode), nullable=False)
    irrigation_state = Column(Enum(IrrigationState), nullable=False)
    heater = Column(Boolean, nullable=False)
    exhaust = Column(Boolean, nullable=False)
    ventilator = Column(Boolean, nullable=False)
    sulfur = Column(Boolean, nullable=False)
    lights = Column(Boolean, nullable=False)
    valves = Column(JSON, nullable=False)
    weather_temperature = Column(Integer, nullable=True)
    weather_humidity = Column(Float, nullable=True)
    weather_sky = Column(String, nullable=True)

    def __repr__(self):
        return f"GreenhouseState(id={self.id!r}, greenhouse_id={self.greenhouse_id!r}, time={self.time!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, quantum={self.quantum!r}, environment_mode={self.environment_mode!r}, environment_statae={self.environment_state!r}, ipm_mode={self.ipm_mode!r}, ipm_state={self.ipm_state!r}, lighting_mode={self.lighting_mode!r}, lighting_state={self.lighting_state!r}, irrigation_mode={self.irrigation_mode!r}, irrigation_state={self.irrigation_state!r}, heater={self.heater!r}, exhaust={self.exhaust!r}, ventilator={self.ventilator!r}, sulfur={self.sulfur!r}, lights={self.lights!r}, valves={self.valves!r}, weather_temperature={self.weather_temperature!r}, weather_humidity={self.weather_humidity!r}, weather_sky={self.weather_sky!r}"


    def to_greenhouse_state(self) -> GreenhouseState:
        return GreenhouseState(
            id=self.id,
            greenhouse_id=self.greenhouse_id,
            time=self.time,
            sensor=Sensor(
                temperature=self.temperature,
                humidity=self.humidity,
                quantum=self.quantum,
            ),
            control=Control(
                environment=Subsystem(
                    mode=self.environment_mode,
                    state=self.environment_state.name,
                ),
                ipm=Subsystem(
                    mode=self.ipm_mode,
                    state=self.ipm_state.name,
                ),
                lighting=Subsystem(
                    mode=self.lighting_mode,
                    state=self.lighting_state.name,
                ),
                irrigation=Subsystem(
                    mode=self.irrigation_mode,
                    state=self.irrigation_state.name,
                ),
            ),
            actuator=Actuator(
                heater=self.heater,
                exhaust=self.exhaust,
                ventilator=self.ventilator,
                sulfur=self.sulfur,
                lights=self.lights,
                valves=self.valves,
            ),
            weather=Weather(
                current=WeatherCurrent(
                    temperature=self.weather_temperature,
                    humidity=self.weather_humidity,
                    sky=self.weather_sky,
                )
            ),
        )


class CreateGreenhouseState(BaseModel):
    sensor: Sensor = None
    control: Control
    actuator: Actuator
    weather: Weather = None

    def to_db_greenhouse_state(self, greenhouse_id: int) -> DbGreenhouseState:
        return DbGreenhouseState(
            greenhouse_id=greenhouse_id,
            temperature=self.sensor.temperature,
            humidity=self.sensor.humidity,
            quantum=self.sensor.quantum,
            environment_mode=self.control.environment.mode,
            environment_state=self.control.environment.state,
            ipm_mode=self.control.ipm.mode,
            ipm_state=self.control.ipm.state,
            lighting_mode=self.control.lighting.mode,
            lighting_state=self.control.lighting.state,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_state=self.control.irrigation.state,
            heater=self.actuator.heater,
            exhaust=self.actuator.exhaust,
            ventilator=self.actuator.ventilator,
            sulfur=self.actuator.sulfur,
            lights=self.actuator.lights,
            valves=self.actuator.valves,
            weather_temperature=self.weather.current.temperature,
            weather_humidity=self.weather.current.humidity,
            weather_sky=self.weather.current.sky,
        )
