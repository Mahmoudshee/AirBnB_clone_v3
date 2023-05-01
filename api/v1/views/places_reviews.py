#!/usr/bin/python3
"""
Handles all default RestFul API actions for Reviews
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req_data = request.get_json()
    user_id = req_data.get('user_id')
    text = req_data.get('text')

    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if text is None:
        return jsonify({"error": "Missing text"}), 400

    req_data['place_id'] = place_id
    review = Review(**req_data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    req_data = request.get_json()
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in req_data.items():
        if key not in ignore:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200


