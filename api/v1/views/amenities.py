#!/usr/bin/python3
"""
Amenities view
"""


from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """get all amenities"""
    states = storage.all(Amenity).values()
    result = []
    for i in states:
        result.append(i.to_dict())

    return(jsonify(result))


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenitie(amenity_id):
    """get selecte amenities """
    Afsa = storage.get(Amenity, amenity_id)
    if Afsa is None:
        abort(404)
    return(jsonify(Afsa.to_dict()))


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """delete amenities"""
    delt = storage.get("Amenity", amenity_id)
    if delt is None:
        abort(404)
    else:
        storage.delete(delt)
        storage.save()
    return make_response(jsonify(), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def Creates_amenities():
    """creates amenities"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    x = request.get_json()
    new_st = Amenity(**x)
    new_st.save()
    return make_response(jsonify(new_st.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def updated_amenities(amenity_id):
    """update states"""
    i = storage.get(Amenity, amenity_id)
    if i is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    x = request.get_json()
    for k, v in x.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(i, k, v)
            storage.save()
    return make_response(jsonify(i.to_dict()), 200)
