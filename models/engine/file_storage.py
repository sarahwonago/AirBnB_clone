#!/usr/bin/python3
""" FileStorage module """

import json
from models.base_model import BaseModel
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review


class FileStorage:
    """
    serializes instances to JSON file and vice versa

    private class attributes:
        __file_path: string file to JSON file
        __objects: dictonary
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the object with key <obj class name>.id
        Attributes:
            obj: <obj class name>.id
        """

        class_word = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(class_word, obj.id)] = obj

    def save(self):
        """ serializes __objects to the JSON file(path: __file_path """
        ourdict = FileStorage.__objects
        our_dict = {obj: ourdict[obj].to_dict() for obj in ourdict.keys()}

        with open(FileStorage.__file_path, "w") as write_file:
            json.dump(our_dict, write_file)

    def reload(self):
        """ deserializes json file to __objects """
        try:
            with open(FileStorage.__file_path) as read_file:
                our_dict = json.load(read_file)
                for i in our_dict.values():
                    class_name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(class_name)(**i))
        except FileNotFoundError:
            return
