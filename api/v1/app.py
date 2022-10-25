#!/usr/bin/python3
"""
    This is the API server module.
"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """errors that returns a JSON-formatted 404 status code"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
