from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    full_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    user = relationship(
        "User",
        back_populates="profile"
    )
