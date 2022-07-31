from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from .shared import Base


class UserGreenhouse(Base):
    __tablename__ = "user_greenhouse"

    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"UserGreenhouse(greenhouse_id={self.greenhouse_id!r}, user_id={self.user_id!r})"
