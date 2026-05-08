from enum import Enum


class Roles(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"
