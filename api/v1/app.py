#!/usr/bin/python3
"""
Sets up Flask application
"""


from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, orgins='0.0.0.0')
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Closes storage session"""
    storage.close()


@app.errorhandler(404)
def handle_bad_request(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True, debug=True)
