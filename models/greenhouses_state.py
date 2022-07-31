from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
import enum
from sqlalchemy import Enum
from .shared import Base

class ControlMode(enum.Enum):
    automatic = 1
    manual = 2

class EnvironmentState(enum.Enum):
    Default = 1

class IpmState(enum.Enum):
    Default = 1

class LightningState(enum.Enum):
    Default = 1

class Weather(enum.Enum):
    Default = 1

class GreenhouseState(Base):
    __tablename__ = "greenhouse_state"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    time = Column(DateTime, nullable=False)
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
