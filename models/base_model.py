#!/usr/bin/python3
"""For every model in our hbnb clone, this module defines a base class."""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class BaseModel:
    """An initial class for every hbnb model"""
    id = Column(String(60), unique=True,
                nullable=False, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instance initiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        elif 'id' not in kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            self.__dict__.update(kwargs)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """provides the instance's string representation back."""
        new_dict = self.__dict__.copy()
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, new_dict)

    def save(self):
        """When an instance changes, updated_at is updated with the current time."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """When an instance is modified, updates updated_at with the current time."""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Change the instance's format to dict"""
        dictionary = {}
        dictionary.update(self.__dict__.copy())
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary
