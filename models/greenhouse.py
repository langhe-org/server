from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
import enum
from sqlalchemy import Enum
from .shared import Base


class GreenhouseType(enum.Enum):
    proto_1_ithaca = 1


class Greenhouse(Base):
    __tablename__ = "greenhouse"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    type = Column(Enum(GreenhouseType), nullable=False)
    location_name = Column(String, nullable=False)
    longitude: Column(Integer, nullable=False)
    latitude: Column(Integer, nullable=False)

    def __repr__(self):
        return f"Greenhouse(id={self.id!r}, name={self.name!r}), type={self.type!r}), location_name={self.location_name!r}), longitude={self.longitude!r}), latitude={self.latitude!r})"
