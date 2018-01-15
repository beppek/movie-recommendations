"""USERS"""

from flask import Blueprint, jsonify
from utils.file_reader import read_ratings, read_users, read_movies
from utils.similarity_calculator import euclidean_distance, pearson_correlation, top_matches, get_recommendations

users = Blueprint('users', __name__)


@users.route('/users')
def get_users():
    """USERS"""

    data = read_users()

    return jsonify(data)

@users.route('/users/ratings')
def get_users_ratings():
    """USERS RATINGS"""

    return jsonify(read_ratings())

@users.route('/users/<_id>/matches')
def user_matches(_id):
    """USER MATCHES"""

    data = top_matches(read_ratings(), _id, 100, pearson_correlation)
    return jsonify(data)

@users.route('/users/<_id>/recommendations/euclidean')
def user_euclidean_recommendations(_id):
    ratings = read_ratings()
    data = get_recommendations(ratings, _id, euclidean_distance)
    return jsonify(data)

@users.route('/users/<_id>/recommendations/pearson')
def user_pearson_recommendations(_id):
    ratings = read_ratings()
    data = get_recommendations(ratings, _id, pearson_correlation)
    return jsonify(data)