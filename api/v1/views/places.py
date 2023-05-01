#!/usr/bin/python3
"""Handles all default RESTful API actions for Place objects."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, User, City, Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.get_json()['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **request.get_json())
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, Place, State, City, Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on the JSON in the body
    of the request"""
    data = request.get_json()
    if not data:
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    if 'states' in data and not all(isinstance(s, str) for s in data['states']):
        abort(400, 'Not a valid state id')

    if 'cities' in data and not all(isinstance(c, str) for c in data['cities']):
        abort(400, 'Not a valid city id')

    if 'amenities' in data and not all(isinstance(a, str) for a in data['amenities']):
        abort(400, 'Not a valid amenity id')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in storage.all(Place).values()])

    place_ids = set()

    # Filter by states
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                for place in city.places:
                    place_ids.add(place.id)

    # Filter by cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                place_ids.add(place.id)

    # Filter by amenities
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            for place in amenity.places:
                place_ids.intersection_update(place_ids, [place.id for place in amenity.places])

    # Retrieve matching Place objects
    places = [storage.get(Place, place_id).to_dict() for place_id in place_ids]

    return jsonify(places)

