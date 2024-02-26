#!/usr/bin/python3
"""
Include the class of FileStorage
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serialises instances and then deserialises them back into instances in a JSON file."""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """provides the __objects dictionary"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def count(self, cls=None):
        """calculate the quantity of storage items."""
        if not cls:
            return len(self.__objects)
        return len(list(filter(lambda o: isinstance(o, cls),
                               self.__objects.values())))

    def get(self, cls, id: str):
        """
        Get Object By Id
        :param cls:
        :param id:
        :return:
        """
        class_object = None
        if (cls):
            for key, value in self.__objects.items():
                if isinstance(value, cls) and value.id == id:
                    return value
        return None

    def new(self, obj):
        """inserts the object with key <obj class name>.id into __objects."""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """converts __objects into a JSON file with the filename __file_path."""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """the JSON file is deserialised to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except BaseException:
            pass

    def delete(self, obj=None):
        """If an object is inside __objects, delete it."""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """use the reload() function to convert the JSON file to objects."""
        self.reload()
