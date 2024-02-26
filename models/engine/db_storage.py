#!/usr/bin/python3
"""
Include the DBStorage class
"""
import urllib.parse

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """deal with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instance intiation a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def get(self, cls, id: str):
        """
        Get Object By Id
        :param cls:
        :param id:
        :return:
        """
        if not cls or not cls:
            return None
        return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """calculate the number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        return sum(map(lambda c: self.__session.query(c).count(),
                       classes.values()))

    def all(self, cls=None):
        """a query regarding the active database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """incorporate the item into the active database session"""
        self.__session.add(obj)

    def save(self):
        """incorporate the item into the active database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """remove from the object in the current database session if none"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """uses the database to refresh data"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Using the private session attribute's delete() method"""
        self.__session.remove()
