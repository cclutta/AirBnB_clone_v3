#!/usr/bin/python3
"""
    This is the cities view.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.state import State

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """
      Displays cities
    """
    state = storage.get(State, state_id)
    if (state):
        if request.method == 'GET':
            return jsonify([c.to_dict() for c in state.cities])
        elif request.method == 'POST':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
                if "name" not in kwargs:
                    return {"error": "Missing name"}, 400
                new_city = City(state_id=state_id, **kwargs)
                new_city.save()
                return new_city.to_dict(), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE', 'PUT', 'GET'])
def city_id(city_id):
    """Get city using its ID. """
    city = storage.get(City, city_id)
    if (city):
        if request.method == 'DELETE':
            city.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, k, v)
            city.save()
        return city.to_dict()
    abort(404)
