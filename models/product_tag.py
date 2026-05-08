from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from database import Base

product_tags = Table(
    "product_tags",
    Base.metadata,

    Column(
        "product_id",
        Integer,
        ForeignKey("products.id")
    ),

    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id")
    )
)
