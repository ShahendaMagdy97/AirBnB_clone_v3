#!/usr/bin/python3
"""
handles status and stats routs
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """returns a JSON confirmation"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """
    retrieveing number of each objects by type
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for key, value in classes.items():
        count_dict[key] = storage.count(value)
    return jsonify(count_dict)
