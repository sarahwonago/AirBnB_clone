#!/usr/bin/python3
"""Module for BaseModel class"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """
    A class that defines all common attributes/methods 
    
    """

    def __init__(self, *args, **kwargs):
        """
        initializes the basemodel class

        """
        dte = '%Y-%m-%dT%H:%M:%S.%f'
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, dte)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):
        """
        prints the string representation of the class

        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute updated_at to the current
        date time

        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation

        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
