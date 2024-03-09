#!/usr/bin/python3
"""
Module that defines all attributes/ methods.
"""
import models
import uuid
from datetime import datetime


class BaseModel:

    """
    Class that defines all attributes/methods.
    Attributes:
        id (str): Unique identifier.
        created_at (datetime): Creation date and time.
        updated_at (datetime): Last update date and time.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes BaseModel Instances
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    self.__dict__[key] = datetime.strptime(value, tform)
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return string representation of BaseModel."""
        return f"[BaseModel] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates attribute updated_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of BaseModel"""
        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__
        model_dict['created_at'] = self.created_at.isoformat()
        model_dict['updated_at'] = self.updated_at.isoformat()
        return model_dict
