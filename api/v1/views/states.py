#!/usr/bin/python3
"""
States  view
"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """get all states"""
    states = storage.all(State).values()
    result = []
    for i in states:
        result.append(i.to_dict())

    return(jsonify(result))


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """get selecte state"""
    Afsa = storage.get(State, state_id)
    if Afsa is None:
        abort(404)
    return(jsonify(Afsa.to_dict()))


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """delete states"""
    delt = storage.get("State", state_id)
    if delt is None:
        abort(404)
    else:
        storage.delete(delt)
        storage.save()
    return make_response(jsonify(), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def Creates_states():
    """creates states"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    x = request.get_json()
    new_st = State(**x)
    new_st.save()
    return make_response(jsonify(new_st.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def updated_states(state_id):
    """update states"""
    i = storage.get(State, state_id)
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
