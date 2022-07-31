from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from .shared import Base

class Units(enum.Enum):
    metric = 1
    imperial = 2


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String, nullable=False)
    units = Column(Enum(Units), nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, units={self.units!r})"
