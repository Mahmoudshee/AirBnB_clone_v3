#!/usr/bin/python3
"""
Creates a Flask application instance
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the database again at the end of the request. """
    storage.close()


@app.route('/api/v1/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

