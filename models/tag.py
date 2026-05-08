from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database import Base
from models.product_tag import product_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    products = relationship(
        "Product",
        secondary=product_tags,
        back_populates="tags"
    )
