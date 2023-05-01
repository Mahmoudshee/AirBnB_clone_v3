#!/usr/bin/python3
"""
Module for the User view.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects.
    """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User.
    """
    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')
    if 'email' not in req_json:
        abort(400, 'Missing email')
    if 'password' not in req_json:
        abort(400, 'Missing password')
    user = User(**req_json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')
    for key, value in req_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())

