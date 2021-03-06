"""USERS"""

from flask import Blueprint, jsonify
from utils.file_reader import read_ratings, read_users, read_movies, read_item_based_data, calc_similar_items
from utils.similarity_calculator import euclidean_distance, pearson_correlation, top_matches, get_recommendations, transform_prefs, get_recommended_items

users = Blueprint('users', __name__)


@users.route('/users')
def get_users():
    """USERS"""

    data = read_users()

    return jsonify(data)

@users.route('/users/ratings')
def get_users_ratings():
    """USERS RATINGS"""

    return jsonify(read_ratings('ratings.csv'))

@users.route('/users/<_id>/matches')
def user_matches(_id):
    """USER MATCHES"""

    data = top_matches(read_ratings('ratings.csv'), _id, 100, pearson_correlation)
    return jsonify(data)

@users.route('/users/<_id>/recommendations/<filtering>/euclidean')
def user_euclidean_recommendations(_id, filtering):
    if filtering == 'user':
        ratings = read_ratings('ratings.csv')
        data = get_recommendations(ratings, _id, euclidean_distance)
    else:
        ratings = read_ratings('ratings.csv')
        item_based = read_item_based_data('euclidean', euclidean_distance, ratings)
        data = get_recommended_items(ratings, item_based, _id)
    return jsonify(data)

@users.route('/users/<_id>/recommendations/<filtering>/pearson')
def user_pearson_recommendations(_id, filtering):
    if filtering == 'user':
        ratings = read_ratings('ratings.csv')
        data = get_recommendations(ratings, _id, pearson_correlation)
    else:
        ratings = read_ratings('ratings.csv')
        item_based = read_item_based_data('pearson', pearson_correlation, ratings)
        data = get_recommended_items(ratings, item_based, _id)
    return jsonify(data)

@users.route('/users/<_id>/test/<filtering>/euclidean')
def test_euclidean_recommendations(_id, filtering):
    if filtering == 'user':
        ratings = read_ratings('ratingstest.csv')
        data = get_recommendations(ratings, _id, euclidean_distance)
    else:
        ratings = read_ratings('ratingstest.csv')
        item_based = read_item_based_data('euclideantest', euclidean_distance, ratings)
        data = get_recommended_items(ratings, item_based, _id)
    return jsonify(data)

@users.route('/users/<_id>/test/<filtering>/pearson')
def test_pearson_recommendations(_id, filtering):
    if filtering == 'user':
        ratings = read_ratings('ratingstest.csv')
        data = get_recommendations(ratings, _id, pearson_correlation)
    else:
        ratings = read_ratings('ratingstest.csv')
        item_based = read_item_based_data('pearsontest', pearson_correlation, ratings)
        data = get_recommended_items(ratings, item_based, _id)
    return jsonify(data)
