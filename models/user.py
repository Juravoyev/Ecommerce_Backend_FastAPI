from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(50), default="buyer")

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False
    )

    products = relationship(
        "Product",
        back_populates="owner"
    )
