#!/usr/bin/python3
"""
    This is the states view.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """
      Displays states
    """
    if request.method == 'GET':
        return jsonify([ob.to_dict() for ob in storage.all("State").values()])
    elif request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        new_state = State(**kwargs)
        new_state.save()
        return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['DELETE', 'PUT', 'GET'])
def state_id(state_id):
    """Get state using its ID. """
    state = storage.get(State, state_id)
    if (state):
        if request.method == 'DELETE':
            state.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)
            state.save()
        return state.to_dict()
    abort(404)
