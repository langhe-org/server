from operator import index
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


class EnvironmentControl(BaseModel):
    mode: ControlMode


class IpmControl(BaseModel):
    mode: ControlMode


class IrrigationControl(BaseModel):
    mode: ControlMode


class LightingControl(BaseModel):
    mode: ControlMode


class Sensor(BaseModel):
    temperature: float = None
    humidity: float = None
    quantum : float = None


class Control(BaseModel):
    environment: EnvironmentControl
    ipm: IpmControl
    lighting: LightingControl
    irrigation: IrrigationControl

class EnvironmentStatus(BaseModel):
    pass


class IpmStatus(BaseModel):
    next_time: datetime = None


class LightingStatus(BaseModel):
    dli: float = None


class IrrigationStatus(BaseModel):
    next_time: datetime = None
    next_zone: int = None


class Status(BaseModel):
    environment: EnvironmentStatus
    ipm: IpmStatus
    lighting: LightingStatus
    irrigation: IrrigationStatus


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
    name: str
    time: time
    duration: timedelta
    sunday: bool
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool


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
    status: Status
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
                index=i,
                valve=self.actuator.valves[i],
                recipe_name=self.recipes.irrigation.zones[i].name,
                recipe_time=self.recipes.irrigation.zones[i].time,
                recipe_duration=self.recipes.irrigation.zones[i].duration,
                recipe_sunday=self.recipes.irrigation.zones[i].sunday,
                recipe_monday=self.recipes.irrigation.zones[i].monday,
                recipe_tuesday=self.recipes.irrigation.zones[i].tuesday,
                recipe_wednesday=self.recipes.irrigation.zones[i].wednesday,
                recipe_thursday=self.recipes.irrigation.zones[i].thursday,
                recipe_friday=self.recipes.irrigation.zones[i].friday,
                recipe_saturday=self.recipes.irrigation.zones[i].saturday,
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
            environment_recipe_day_temperature=self.recipes.environment.day_temperature,
            environment_recipe_night_temperature=self.recipes.environment.night_temperature,
            environment_recipe_humidity_limit=self.recipes.environment.humidity_limit,
            ipm_mode=self.control.ipm.mode,
            ipm_recipe_intensity=self.recipes.ipm.intensity,
            ipm_status_next_time=self.status.ipm.next_time,
            lighting_mode=self.control.lighting.mode,
            lighting_recipe_start_at=self.recipes.lighting.start_at,
            lighting_recipe_stop_at=self.recipes.lighting.stop_at,
            lighting_recipe_intensity=self.recipes.lighting.intensity,
            lighting_status_dli=self.status.lighting.dli,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_zones=irrigation_zones,
            irrigation_status_next_time=self.status.irrigation.next_time,
            irrigation_status_next_zone=self.status.irrigation.next_zone,
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
    index = Column(Integer, nullable=False)
    valve = Column(Boolean, nullable=False)
    recipe_name = Column(String, nullable=False)
    recipe_time = Column(Time, nullable=False)
    recipe_duration = Column(Integer, nullable=False)
    recipe_sunday = Column(Boolean, nullable=False)
    recipe_monday = Column(Boolean, nullable=False)
    recipe_tuesday = Column(Boolean, nullable=False)
    recipe_wednesday = Column(Boolean, nullable=False)
    recipe_thursday = Column(Boolean, nullable=False)
    recipe_friday = Column(Boolean, nullable=False)
    recipe_saturday = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"DbGreenhouseStateIrrigation(id={self.id!r}, greenhouse_state_id={self.greenhouse_state_id!r}, valve={self.valve!r}, time={self.time!r}, duration={self.duration!r}, sunday={self.sunday!r}, monday={self.monday!r}, tuesday={self.tuesday!r}, wednesday={self.wednesday!r}, thursday={self.thursday!r}, friday={self.friday!r}, saturday={self.saturday!r}"


class DbGreenhouseState(Base):
    __tablename__ = "greenhouse_state"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    time = Column(DateTime, nullable=False, index=True, server_default=func.now())
    temperature = Column(Integer, nullable=False)
    humidity = Column(Float, nullable=False)
    quantum = Column(Float, nullable=False)
    environment_mode = Column(Enum(ControlMode), nullable=False)
    environment_recipe_day_temperature = Column(Float, nullable=False)
    environment_recipe_night_temperature = Column(Float, nullable=False)
    environment_recipe_humidity_limit = Column(Float, nullable=False)
    ipm_mode = Column(Enum(ControlMode), nullable=False)
    ipm_recipe_intensity = Column(Enum(SulfurIntensity), nullable=False)
    ipm_status_next_time = Column(DateTime, nullable=True)
    lighting_mode = Column(Enum(ControlMode), nullable=False)
    lighting_recipe_start_at = Column(Time, nullable=False)
    lighting_recipe_stop_at = Column(Time, nullable=False)
    lighting_recipe_intensity = Column(Enum(LightingRecipeIntensity), nullable=False)
    lighting_status_dli = Column(Float, nullable=True)
    irrigation_mode = Column(Enum(ControlMode), nullable=False)
    irrigation_zones = relationship("DbGreenhouseStateIrrigation", back_populates="greenhouse_state", order_by="DbGreenhouseStateIrrigation.index")
    irrigation_status_next_time = Column(DateTime, nullable=True)
    irrigation_status_next_zone = Column(Integer, nullable=True)
    heater = Column(Boolean, nullable=False)
    exhaust = Column(Boolean, nullable=False)
    ventilator = Column(Boolean, nullable=False)
    sulfur = Column(Boolean, nullable=False)
    lights = Column(Boolean, nullable=False)
    weather_temperature = Column(Integer, nullable=True)
    weather_humidity = Column(Float, nullable=True)
    weather_sky = Column(String, nullable=True)

    def __repr__(self):
        return f"GreenhouseState(id={self.id!r}, greenhouse_id={self.greenhouse_id!r}, time={self.time!r}, temperature={self.temperature!r}, humidity={self.humidity!r}, quantum={self.quantum!r}, environment_mode={self.environment_mode!r}, environment_recipe_day_temperature={self.environment_recipe_day_temperature!r}, environment_recipe_night_temperature={self.environment_recipe_night_temperature!r}, environment_recipe_humidity_limit={self.environment_recipe_humidity_limit!r}, ipm_mode={self.ipm_mode!r}, ipm_recipe_intensity={self.ipm_recipe_intensity!r}, lighting_mode={self.lighting_mode!r}, lighting_recipe_start_at={self.lighting_recipe_start_at!r}, lighting_recipe_stop_at={self.lighting_recipe_stop_at!r}, lighting_recipe_intensity={self.lighting_recipe_intensity!r}, irrigation_mode={self.irrigation_mode!r}, irrigation_zones={self.irrigation_zones!r}, heater={self.heater!r}, exhaust={self.exhaust!r}, ventilator={self.ventilator!r}, sulfur={self.sulfur!r}, lights={self.lights!r}, weather_temperature={self.weather_temperature!r}, weather_humidity={self.weather_humidity!r}, weather_sky={self.weather_sky!r}"

    def to_greenhouse_state(self) -> GreenhouseState:
        irrigation_recipe_zones = [IrrigationRecipeZone(
            name=irrigation_valve.recipe_name,
            time=irrigation_valve.recipe_time,
            duration=irrigation_valve.recipe_duration,
            sunday=irrigation_valve.recipe_sunday,
            monday=irrigation_valve.recipe_monday,
            tuesday=irrigation_valve.recipe_tuesday,
            wednesday=irrigation_valve.recipe_wednesday,
            thursday=irrigation_valve.recipe_thursday,
            friday=irrigation_valve.recipe_friday,
            saturday=irrigation_valve.recipe_saturday,
        ) for irrigation_valve in self.irrigation_zones]

        irrigation_zones = [ zone.valve for zone in self.irrigation_zones]

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
                environment=EnvironmentControl(
                    mode=self.environment_mode,
                ),
                ipm=IpmControl(
                    mode=self.ipm_mode,
                ),
                lighting=LightingControl(
                    mode=self.lighting_mode,
                ),
                irrigation=IrrigationControl(
                    mode=self.irrigation_mode,
                ),
            ),
            status=Status(
                environment=EnvironmentStatus(),
                ipm=IpmStatus(
                    next_time=self.ipm_status_next_time,
                ),
                lighting=LightingStatus(
                    dli=self.lighting_status_dli,
                ),
                irrigation=IrrigationStatus(
                    next_time=self.irrigation_status_next_time,
                    next_zone=self.irrigation_status_next_zone,
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
    status: Status
    recipes: Recipes
    actuator: Actuator
    weather: Weather = None

    def to_db_greenhouse_state(self, greenhouse_id: int) -> DbGreenhouseState:
        if len(self.recipes.irrigation.zones) != len(self.actuator.valves):
            raise Exception("Recipe irrigation length not equal to valves length")

        irrigation_zones = list(map(
            lambda i: DbGreenhouseStateIrrigation(
                index=i,
                valve=self.actuator.valves[i],
                recipe_name=self.recipes.irrigation.zones[i].name,
                recipe_time=self.recipes.irrigation.zones[i].time,
                recipe_duration=self.recipes.irrigation.zones[i].duration,
                recipe_sunday=self.recipes.irrigation.zones[i].sunday,
                recipe_monday=self.recipes.irrigation.zones[i].monday,
                recipe_tuesday=self.recipes.irrigation.zones[i].tuesday,
                recipe_wednesday=self.recipes.irrigation.zones[i].wednesday,
                recipe_thursday=self.recipes.irrigation.zones[i].thursday,
                recipe_friday=self.recipes.irrigation.zones[i].friday,
                recipe_saturday=self.recipes.irrigation.zones[i].saturday,
            ),
            range(len(self.actuator.valves)),
        ))

        return DbGreenhouseState(
            greenhouse_id=greenhouse_id,
            temperature=self.sensor.temperature,
            humidity=self.sensor.humidity,
            quantum=self.sensor.quantum,
            environment_mode=self.control.environment.mode,
            environment_recipe_day_temperature=self.recipes.environment.day_temperature,
            environment_recipe_night_temperature=self.recipes.environment.night_temperature,
            environment_recipe_humidity_limit=self.recipes.environment.humidity_limit,
            ipm_mode=self.control.ipm.mode,
            ipm_recipe_intensity=self.recipes.ipm.intensity,
            ipm_status_next_time=self.status.ipm.next_time,
            lighting_mode=self.control.lighting.mode,
            lighting_recipe_start_at=self.recipes.lighting.start_at,
            lighting_recipe_stop_at=self.recipes.lighting.stop_at,
            lighting_recipe_intensity=self.recipes.lighting.intensity,
            lighting_status_dli=self.status.lighting.dli,
            irrigation_mode=self.control.irrigation.mode,
            irrigation_zones=irrigation_zones,
            irrigation_status_next_time=self.status.irrigation.next_time,
            irrigation_status_next_zone=self.status.irrigation.next_zone,
            heater=self.actuator.heater,
            exhaust=self.actuator.exhaust,
            ventilator=self.actuator.ventilator,
            sulfur=self.actuator.sulfur,
            lights=self.actuator.lights,
            weather_temperature=self.weather.current.temperature,
            weather_humidity=self.weather.current.humidity,
            weather_sky=self.weather.current.sky,
        )
