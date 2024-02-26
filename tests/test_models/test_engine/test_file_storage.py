#!/usr/bin/python3
"""
comprises the classes TestFileStorageDocs.
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to verify the FileStorage class's documentation and style"""

    @classmethod
    def setUpClass(cls):
        """Organise the document tests."""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Verify that file_storage.py and models/engine/complies with PEP8.
"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "found warnings and mistakes in the code style")

    def test_pep8_conformance_test_file_storage(self):
        """The file test_file_storage.py and test_models/test_models.py follow PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "detected warnings and problems in the code style.")

    def test_file_storage_module_docstring(self):
        """Test for the docstring module file_storage.py"""
        self.assertIsNot(file_storage.__doc__, None,
                         "A docstring is required for file_storage.py.")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "There is no docstring for file_storage.py.")

    def test_file_storage_class_docstring(self):
        """Test for the docstring FileStorage class"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "The FileStorage class requires a docstring.")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class requires a document string")

    def test_fs_func_docstrings(self):
        """Verify if the FileStorage methods contain docstrings."""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Examine the class FileStorage."""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Verify that every one of the FileStorage.__objects attr returns."""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that updates the FileStorage.__objects attr with a new object"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Verify that the items are correctly saved to a file.JSON"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing DB storage")
    def test_count(self):
        """The count test yields the quantity of objects stored in storage."""
        storage = FileStorage()
        count = storage.count()
        self.assertEqual(type(count), int)
        self.assertEqual(count, len(storage.all()))

    @unittest.skipIf(models.storage_t == 'db', "not testing DB storage")
    def test_get(self):
        """Test that retrieves the item by using its ID and class name"""
        storage = FileStorage()
        name = "Californiaaaaaaaaaaaa"
        state = State(name="Californiaaaaaaaaaaaa")
        state.save()
        state_id = state.id
        state_name = state.name
        get_state = storage.get(State, state_id)
        self.assertEqual(state.name, name)
        self.assertEqual(state_id, get_state.id)
        self.assertEqual(state_name, get_state.name)
