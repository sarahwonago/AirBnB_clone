#!/usr/bin/python3
"""Define Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents amenity.

    Attributes:
        name (str): amenity name.
    """

    name = ""
