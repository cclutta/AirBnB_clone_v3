#!/usr/bin/python3
"""
    This is the amenities view.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """
      Displays amenities
    """
    if request.method == 'GET':
        return jsonify([o.to_dict() for o in storage.all("Amenity").values()])
    elif request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        new_amenity = Amenity(**kwargs)
        new_amenity.save()
        return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE', 'PUT', 'GET'])
def amenity_id(amenity_id):
    """Get amenity using its ID. """
    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        if request.method == 'DELETE':
            amenity.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, k, v)
            amenity.save()
        return amenity.to_dict()
    abort(404)
