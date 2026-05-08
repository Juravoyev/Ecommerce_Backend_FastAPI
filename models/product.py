from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database import Base
from models.product_tag import product_tags


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(String)

    price = Column(Float)

    image = Column(String, nullable=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    owner = relationship(
        "User",
        back_populates="products"
    )

    tags = relationship(
        "Tag",
        secondary=product_tags,
        back_populates="products"
    )
