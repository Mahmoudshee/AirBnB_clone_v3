#!/usr/bin/python3
"""
Creates a Flask application instance
"""

from flask import Flask, jsonify
from models import storage
import os

app = Flask(__name__)

@app.teardown_appcontext
def close_storage(error):
    storage.close()

@app.route('/api/v1/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    from api.v1.views import app_views
    app.register_blueprint(app_views)
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', 5000)),
            threaded=True)

