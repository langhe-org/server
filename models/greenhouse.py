from sqlalchemy import Column, String, Integer, Enum
import enum
from .db_base import Base
from pydantic import BaseModel


class GreenhouseType(enum.Enum):
    proto_1_ithaca = 1


class Greenhouse(BaseModel):
    id: int
    name: str = None
    type: GreenhouseType
    location_name: str = None
    longitude: int
    latitude: int

    class Config:
        orm_mode = True

    def to_db_greenhouse(self): # can the return type be strongly typed?
        return DbGreenhouse(id=self.id, name=self.name, type=self.type, location_name=self.location_name, longitude=self.longitude, latitude=self.latitude)


class DbGreenhouse(Base):
    __tablename__ = "greenhouse"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    type = Column(Enum(GreenhouseType), nullable=False)
    location_name = Column(String, nullable=False)
    longitude = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Greenhouse(id={self.id!r}, name={self.name!r}), type={self.type!r}), location_name={self.location_name!r}), longitude={self.longitude!r}), latitude={self.latitude!r})"

    def to_greenhouse(self) -> Greenhouse:
        return Greenhouse(id=self.id, name=self.name, type=self.type, location_name=self.location_name, longitude=self.longitude, latitude=self.latitude)


class CreateGreenhouse(BaseModel):
    name: str = None
    type: GreenhouseType
    location_name: str = None
    longitude: int
    latitude: int

    class Config:
        orm_mode = True

    def to_db_greenhouse(self) -> DbGreenhouse:
        return DbGreenhouse(name=self.name, type=self.type, location_name=self.location_name, longitude=self.longitude, latitude=self.latitude)


class UpdateGreenhouse(BaseModel):
    name: str = None
    location_name: str = None
    longitude: int = None
    latitude: int = None

    class Config:
        orm_mode = True
