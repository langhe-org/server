from sqlalchemy import Column, Integer, Enum, String
import enum
from pydantic import BaseModel, EmailStr

from .db_base import Base

class Units(enum.Enum):
    metric = "metric"
    imperial = "imperial"


class User(BaseModel):
    id: int
    name: str = None
    email: EmailStr
    units: Units = Units.imperial

    class Config:
        orm_mode = True

    def to_db_user(self): # can the return type be strongly typed?
        return DbUser(id=self.id, name=self.name, email=self.email, units=self.units)


class DbUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String, nullable=False)
    units = Column(Enum(Units), nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, units={self.units!r})"

    def to_user(self) -> User:
        return User(id=self.id, name=self.name, email=self.email, units=self.units)


class UpdateUser(BaseModel):
    name: str = None
    email: EmailStr
    units: Units = Units.imperial

    class Config:
        orm_mode = True
