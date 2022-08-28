from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, DateTime, Time, String, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from typing import List, Generic, TypeVar
import enum
from .db_base import Base
from pydantic import BaseModel
from datetime import datetime, time, timedelta
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


class EnvironmentRecipe(BaseModel):
    day_temperature: float
    night_temperature: float
    humidity_limit: float


class SulfurIntensity(enum.Enum):
    off = "off"
    low = "low"
    medium = "medium"
    high = "high"


class IpmRecipe(BaseModel):
    intensity: SulfurIntensity


class LightingRecipeIntensity(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class LightingRecipe(BaseModel):
    start_at: time
    stop_at: time
    intensity: LightingRecipeIntensity


class IrrigationRecipeZone(BaseModel):
    start_window: time
    stop_window: time
    duration: timedelta
    frequency: timedelta


class IrrigationRecipe(BaseModel):
    zones: List[IrrigationRecipeZone]


class Recipes(BaseModel):
    environment: EnvironmentRecipe
    ipm: IpmRecipe
    lighting: LightingRecipe
    irrigation: IrrigationRecipe


class GreenhouseState(BaseModel):
    id: int
    greenhouse_id: int
    time: datetime
    sensor: Sensor = None
    control: Control
    recipes: Recipes
    actuator: Actuator
    weather: Weather = None

    class Config:
        orm_mode = True

    def to_db_greenhouse_state(self): # can the return type be strongly typed?
        if len(self.recipes.irrigation.zones) != len(self.actuator.valves):
            raise Exception("Recipe irrigation length not equal to valves length")

        irrigation_zones = list(map(
            lambda i: DbGreenhouseStateIrrigation(
                valve=self.actuator.valves[i],
                recipe_start_window=self.recipes.irrigation.zones[i].start_window,
                recipe_stop_window=self.recipes.irrigation.zones[i].stop_window,
                recipe_duration=self.recipes.irrigation.zones[i].duration,
                recipe_frequency=self.recipes.irrigation.zones[i].frequency,
            ),
            range(len(self.actuator.valves)),
        ))

        return DbGreenhouseState(
            id=self.id,
            greenhouse_id=self.greenhouse_id,
            time=self.time,
            temperature=self.sensor.temperature,
            humidity=self.sensor.humidity,
            quantum=self.sensor.quantum,
            environment_mode=self.control.environment.mode,
            environment_state=self.control.environment.state,
            environment_recipe_day_temperature=self.recipes.environment.day_temperature,
            environment_recipe_night_temperature=self.recipes.environment.night_temperature,
            environment_recipe_humidity_limit=self.recipes.environment.humidity_limit,
            ipm_mode=self.control.ipm.mode,
            ipm_state=self.control.ipm.state,
            ipm_recipe_intensity=self.recipes.ipm.intensity,
            lighting_mode=self.control.lighting.mode,
            lighting_state=self.control.lighting.state,
            lighting_recipe_start_at=self.recipes.lighting.start_at,
            lighting_recipe_stop_at=self.recipes.lighting.stop_at,
            lighting_recipe_intensity=self.recipes.lighting.intensity,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_state=self.control.irrigation.state,
            irrigation_zones=irrigation_zones,
            heater=self.actuator.heater,
            exhaust=self.actuator.exhaust,
            ventilator=self.actuator.ventilator,
            sulfur=self.actuator.sulfur,
            lights=self.actuator.lights,
            weather_temperature=self.weather.current.temperature,
            weather_humidity=self.weather.current.humidity,
            weather_sky=self.weather.current.sky,
        )


class DbGreenhouseStateIrrigation(Base):
    __tablename__ = "greenhouse_state_irrigation"

    id = Column(Integer, primary_key=True)
    greenhouse_state_id = Column(Integer, ForeignKey("greenhouse_state.id"), nullable=False)
    greenhouse_state = relationship("DbGreenhouseState", back_populates="irrigation_zones")
    valve = Column(Boolean, nullable=False)
    recipe_start_window = Column(Time, nullable=False)
    recipe_stop_window = Column(Time, nullable=False)
    recipe_duration = Column(postgresql.INTERVAL(), nullable=False)
    recipe_frequency = Column(postgresql.INTERVAL(), nullable=False)

    def __repr__(self):
        return f"DbGreenhouseStateIrrigation(id={self.id!r}, greenhouse_state_id={self.greenhouse_state_id!r}, valve={self.valve!r}, recipe_start_window={self.recipe_start_window!r}, recipe_stop_window={self.recipe_stop_window!r}, recipe_duration={self.recipe_duration!r}"


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
    environment_recipe_day_temperature = Column(Float, nullable=False)
    environment_recipe_night_temperature = Column(Float, nullable=False)
    environment_recipe_humidity_limit = Column(Float, nullable=False)
    ipm_mode = Column(Enum(ControlMode), nullable=False)
    ipm_state = Column(Enum(IpmState), nullable=False)
    ipm_recipe_intensity = Column(Enum(SulfurIntensity), nullable=False)
    lighting_mode = Column(Enum(ControlMode), nullable=False)
    lighting_state = Column(Enum(LightningState), nullable=False)
    lighting_recipe_start_at = Column(Time, nullable=False)
    lighting_recipe_stop_at = Column(Time, nullable=False)
    lighting_recipe_intensity = Column(Enum(LightingRecipeIntensity), nullable=False)
    irrigation_mode = Column(Enum(ControlMode), nullable=False)
    irrigation_state = Column(Enum(IrrigationState), nullable=False)
    irrigation_zones = relationship("DbGreenhouseStateIrrigation", back_populates="greenhouse_state")
    heater = Column(Boolean, nullable=False)
    exhaust = Column(Boolean, nullable=False)
    ventilator = Column(Boolean, nullable=False)
    sulfur = Column(Boolean, nullable=False)
    lights = Column(Boolean, nullable=False)
    weather_temperature = Column(Integer, nullable=True)
    weather_humidity = Column(Float, nullable=True)
    weather_sky = Column(String, nullable=True)

    def __repr__(self):
        return f"GreenhouseState(id={self.id!r}, greenhouse_id={self.greenhouse_id!r}, time={self.time!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, quantum={self.quantum!r}, environment_mode={self.environment_mode!r}, environment_state={self.environment_state!r}, environment_recipe_day_temperature={self.environment_recipe_day_temperature!r}, environment_recipe_night_temperature={self.environment_recipe_night_temperature!r}, environment_recipe_humidity_limit={self.environment_recipe_humidity_limit!r}, ipm_mode={self.ipm_mode!r}, ipm_state={self.ipm_state!r}, ipm_recipe_intensity={self.ipm_recipe_intensity!r}, lighting_mode={self.lighting_mode!r}, lighting_state={self.lighting_state!r}, lighting_recipe_start_at={self.lighting_recipe_start_at!r}, lighting_recipe_stop_at={self.lighting_recipe_stop_at!r}, lighting_recipe_intensity={self.lighting_recipe_intensity!r}, irrigation_mode={self.irrigation_mode!r}, irrigation_state={self.irrigation_state!r}, irrigation_zones={self.irrigation_zones!r}, heater={self.heater!r}, exhaust={self.exhaust!r}, ventilator={self.ventilator!r}, sulfur={self.sulfur!r}, lights={self.lights!r}, weather_temperature={self.weather_temperature!r}, weather_humidity={self.weather_humidity!r}, weather_sky={self.weather_sky!r}"

    def to_greenhouse_state(self) -> GreenhouseState:
        irrigation_recipe_zones = list(map(
            lambda irrigation_valve: IrrigationRecipeZone(
                start_window=irrigation_valve.recipe_start_window,
                stop_window=irrigation_valve.recipe_stop_window,
                duration=irrigation_valve.recipe_duration,
                frequency=irrigation_valve.recipe_frequency,
            ),
            self.irrigation_zones,
        ))
        irrigation_zones = list(map(
            lambda irrigation_valve: irrigation_valve.valve,
            self.irrigation_zones,
        ))

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
            recipes=Recipes(
                environment = EnvironmentRecipe(
                    day_temperature=self.environment_recipe_day_temperature,
                    night_temperature=self.environment_recipe_night_temperature,
                    humidity_limit=self.environment_recipe_humidity_limit,
                ),
                ipm = IpmRecipe(
                    intensity=self.ipm_recipe_intensity,
                ),
                lighting = LightingRecipe(
                    start_at=self.lighting_recipe_start_at,
                    stop_at=self.lighting_recipe_stop_at,
                    intensity=self.lighting_recipe_intensity,
                ),
                irrigation = IrrigationRecipe(
                    zones=irrigation_recipe_zones,
                ),
            ),
            actuator=Actuator(
                heater=self.heater,
                exhaust=self.exhaust,
                ventilator=self.ventilator,
                sulfur=self.sulfur,
                lights=self.lights,
                valves=irrigation_zones,
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
    recipes: Recipes
    actuator: Actuator
    weather: Weather = None

    def to_db_greenhouse_state(self, greenhouse_id: int) -> DbGreenhouseState:
        if len(self.recipes.irrigation.zones) != len(self.actuator.valves):
            raise Exception("Recipe irrigation length not equal to valves length")

        irrigation_zones = list(map(
            lambda i: DbGreenhouseStateIrrigation(
                valve=self.actuator.valves[i],
                recipe_start_window=self.recipes.irrigation.zones[i].start_window,
                recipe_stop_window=self.recipes.irrigation.zones[i].stop_window,
                recipe_duration=self.recipes.irrigation.zones[i].duration,
                recipe_frequency=self.recipes.irrigation.zones[i].frequency,
            ),
            range(len(self.actuator.valves)),
        ))

        return DbGreenhouseState(
            greenhouse_id=greenhouse_id,
            temperature=self.sensor.temperature,
            humidity=self.sensor.humidity,
            quantum=self.sensor.quantum,
            environment_mode=self.control.environment.mode,
            environment_state=self.control.environment.state,
            environment_recipe_day_temperature=self.recipes.environment.day_temperature,
            environment_recipe_night_temperature=self.recipes.environment.night_temperature,
            environment_recipe_humidity_limit=self.recipes.environment.humidity_limit,
            ipm_mode=self.control.ipm.mode,
            ipm_state=self.control.ipm.state,
            ipm_recipe_intensity=self.recipes.ipm.intensity,
            lighting_mode=self.control.lighting.mode,
            lighting_state=self.control.lighting.state,
            lighting_recipe_start_at=self.recipes.lighting.start_at,
            lighting_recipe_stop_at=self.recipes.lighting.stop_at,
            lighting_recipe_intensity=self.recipes.lighting.intensity,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_state=self.control.irrigation.state,
            irrigation_zones=irrigation_zones,
            heater=self.actuator.heater,
            exhaust=self.actuator.exhaust,
            ventilator=self.actuator.ventilator,
            sulfur=self.actuator.sulfur,
            lights=self.actuator.lights,
            weather_temperature=self.weather.current.temperature,
            weather_humidity=self.weather.current.humidity,
            weather_sky=self.weather.current.sky,
        )
