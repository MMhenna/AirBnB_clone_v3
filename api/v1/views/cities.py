#!/usr/bin/python3
"""
City view
"""


from os import stat
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_city(state_id):
    """get all cities"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    cities = storage.all(City).values() 
    result = []
    for i in cities:
        if i.state_id == state_id:
            result.append(i.to_dict())

    return(jsonify(result))

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_state(city_id):
    """get selecte state"""
    Afsa = storage.get(City, city_id)
    if Afsa is None:
        abort(404)
    return(jsonify(Afsa.to_dict()))


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(city_id):
    """delete states"""
    delt = storage.get(City, city_id)
    if delt is None:
        abort(404)
    else:
        storage.delete(delt)
        storage.save()
    return make_response(jsonify(), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def Creates_states(state_id):
    """creates states"""
    sta = storage.get(State, state_id)
    if sta is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    x = request.get_json
    new_st = City(**x)
    new_st.state_id = state_id
    new_st.save()
    return make_response(jsonify(new_st.to_dict), 200)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def updated_states(city_id):
    """update states"""
    i = storage.get(City, city_id)
    if i is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    x = request.get_json
    for k, v in x.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(i, k, v)
            storage.save()
    return make_response(jsonify(i.to_dict), 200)
