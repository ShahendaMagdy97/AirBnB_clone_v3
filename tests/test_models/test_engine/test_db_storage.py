#!/usr/bin/python3
"""
Include the Test DBStorageDocs and Test DBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to verify the DBStorage class's documentation and style"""

    @classmethod
    def setUpClass(cls):
        """Organise the document tests."""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Verify the models/engine/db_storage.py file's compliance with PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "detected warnings and problems in the code style.")

    def test_pep8_conformance_test_db_storage(self):
        """The test files tests/test_models/test_db_storage.py are PEP8 compliant."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "found warnings and mistakes in the code style.")

    def test_db_storage_module_docstring(self):
        """Test for docstring module db_storage.py"""
        self.assertIsNot(db_storage.__doc__, None,
                         "Docstring required for db_storage.py")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "There is no docstring for db_storage.py.")

    def test_db_storage_class_docstring(self):
        """Test for the docstring DBStorage class"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "The DBStorage class requires a docstring.")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "docstoring is needed for DBStorage class")

    def test_dbs_func_docstrings(self):
        """Verify whether docstrings are present in DBStorage methods."""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_get(self):
        """Test that retrieves the item by using its ID and class name
"""
        from models import storage as db_storage
        name = "Californiaaaaaaaaaaa"
        state = State(name="Californiaaaaaaaaaaa")
        state.save()
        state_id = state.id
        state_name = state.name
        get_state = db_storage.get(State, state_id)
        self.assertEqual(state.name, name)
        self.assertEqual(state_id, get_state.id)
        self.assertEqual(state_name, get_state.name)

    def test_count(self):
        """The count test yields the quantity of objects stored in storage.
"""
        from models import storage as db_storage
        storage = db_storage
        count = storage.count()
        self.assertEqual(type(count), int)
        self.assertEqual(count, len(storage.all()))
