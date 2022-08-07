from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, DateTime, Enum, func
import enum
from .db_base import Base
from pydantic import BaseModel
from datetime import datetime


class ControlMode(enum.Enum):
    automatic = "automatic"
    manual = "manual"


class EnvironmentState(enum.Enum):
    Default = "Default" # change to lowercase


class IpmState(enum.Enum):
    Default = "Default" # change to lowercase


class LightningState(enum.Enum):
    Default = "Default" # change to lowercase


class Weather(enum.Enum):
    Default = 1


class GreenhouseState(BaseModel):
    id: int
    greenhouse_id: int # TODO: full greenhouse?
    time: datetime
    timezone: float
    dst: bool
    temperature: int
    humidity: float
    quantum: int
    environment_mode: ControlMode
    environment_state: EnvironmentState
    ipm_mode: ControlMode
    ipm_state: IpmState
    lighting_mode: ControlMode
    lighting_state: LightningState
    heater: bool
    exhaust: bool
    ventilator: bool
    sulfur: bool
    weather_temperature: int = None
    weather_humidity: float = None
    weather_sky: Weather = None
    push_seconds: int = 60

    class Config:
        orm_mode = True

    def to_db_greenhouse_state(self): # can the return type be strongly typed?
        return DbGreenhouseState(id=self.id, greenhouse_id=self.greenhouse_id, time=self.time, timezone=self.timezone, dst=self.dst, temperature=self.temperature, humidity=self.humidity, quantum=self.quantum, environment_mode=self.environment_mode, environment_state=self.environment_state, ipm_mode=self.ipm_mode, ipm_state=self.ipm_state, lighting_mode=self.lighting_mode, lighting_state=self.lighting_state, heater=self.heater, exhaust=self.exhaust, ventilator=self.ventilator, sulfur=self.sulfur, weather_temperature=self.weather_temperature, weather_humidity=self.weather_humidity, weather_sky=self.weather_sky, push_seconds=self.push_seconds)


class DbGreenhouseState(Base):
    __tablename__ = "greenhouse_state"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    time = Column(DateTime, nullable=False, index=True, server_default=func.now())
    timezone = Column(Float, nullable=False)
    dst = Column(Boolean, nullable=False)
    temperature = Column(Integer, nullable=False)
    humidity = Column(Float, nullable=False)
    quantum = Column(Integer, nullable=False)
    environment_mode = Column(Enum(ControlMode), nullable=False)
    environment_state = Column(Enum(EnvironmentState), nullable=False)
    ipm_mode = Column(Enum(ControlMode), nullable=False)
    ipm_state = Column(Enum(IpmState), nullable=False)
    lighting_mode = Column(Enum(ControlMode), nullable=False)
    lighting_state = Column(Enum(LightningState), nullable=False)
    heater = Column(Boolean, nullable=False)
    exhaust = Column(Boolean, nullable=False)
    ventilator = Column(Boolean, nullable=False)
    sulfur = Column(Boolean, nullable=False)
    weather_temperature = Column(Integer, nullable=True)
    weather_humidity = Column(Float, nullable=True)
    weather_sky = Column(Enum(Weather), nullable=True)
    push_seconds = Column(Integer, nullable=False)

    def __repr__(self):
        return f"GreenhouseState(id={self.id!r}, email_address={self.email_address!r})"

    def to_greenhouse_state(self) -> GreenhouseState:
        return GreenhouseState(id=self.id, greenhouse_id=self.greenhouse_id, time=self.time, timezone=self.timezone, dst=self.dst, temperature=self.temperature, humidity=self.humidity, quantum=self.quantum, environment_mode=self.environment_mode, environment_state=self.environment_state, ipm_mode=self.ipm_mode, ipm_state=self.ipm_state, lighting_mode=self.lighting_mode, lighting_state=self.lighting_state, heater=self.heater, exhaust=self.exhaust, ventilator=self.ventilator, sulfur=self.sulfur, weather_temperature=self.weather_temperature, weather_humidity=self.weather_humidity, weather_sky=self.weather_sky, push_seconds=self.push_seconds)


class CreateGreenhouseState(BaseModel):
    timezone: float
    dst: bool
    temperature: int
    humidity: float
    quantum: int
    environment_mode: ControlMode
    environment_state: EnvironmentState
    ipm_mode: ControlMode
    ipm_state: IpmState
    lighting_mode: ControlMode
    lighting_state: LightningState
    heater: bool
    exhaust: bool
    ventilator: bool
    sulfur: bool
    weather_temperature: int = None
    weather_humidity: float = None
    weather_sky: Weather = None
    push_seconds: int = 60

    def to_db_greenhouse_state(self, greenhouse_id: int) -> DbGreenhouseState:
        return DbGreenhouseState(greenhouse_id=greenhouse_id, timezone=self.timezone, dst=self.dst, temperature=self.temperature, humidity=self.humidity, quantum=self.quantum, environment_mode=self.environment_mode, environment_state=self.environment_state, ipm_mode=self.ipm_mode, ipm_state=self.ipm_state, lighting_mode=self.lighting_mode, lighting_state=self.lighting_state, heater=self.heater, exhaust=self.exhaust, ventilator=self.ventilator, sulfur=self.sulfur, weather_temperature=self.weather_temperature, weather_humidity=self.weather_humidity, weather_sky=self.weather_sky, push_seconds=self.push_seconds)
