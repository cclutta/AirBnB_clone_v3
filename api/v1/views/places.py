#!/usr/bin/python3
"""
    This is the amenities view.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """
      Displays users
    """
    if request.method == 'GET':
        return jsonify([o.to_dict() for o in storage.all("User").values()])
    elif request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        new_user = User(**kwargs)
        new_user.save()
        return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['DELETE', 'PUT', 'GET'])
def user_id(user_id):
    """Get amenity using its ID. """
    user = storage.get(User, user_id)
    if (user):
        if request.method == 'DELETE':
            user.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(user, k, v)
            user.save()
        return user.to_dict()
    abort(404)
