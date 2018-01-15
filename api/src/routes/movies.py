"""MOVIES"""

from flask import Blueprint, jsonify
from utils.file_reader import read_ratings, read_users, read_movies
from utils.similarity_calculator import euclidean_distance, pearson_correlation, top_matches, get_recommendations, transform_prefs

movies = Blueprint('movies', __name__)

@movies.route('/movies')
def get_users():
    """MOVIES"""

    data = read_movies()

    return jsonify(data)

@movies.route('/movies/<_id>/recommendations/euclidean')
def movies_euclidean_recommendations(_id):
    ratings = read_ratings()
    mov = read_movies()
    movie_based_ratings = transform_prefs(ratings)
    # return jsonify(movie_based_ratings)
    data = top_matches(movie_based_ratings, mov[_id]['title'], 500, euclidean_distance)
    return jsonify({'recommendations': data})
@movies.route('/movies/<_id>/recommendations/pearson')
def movies_pearson_recommendations(_id):
    ratings = read_ratings()
    mov = read_movies()
    movie_based_ratings = transform_prefs(ratings)
    data = top_matches(movie_based_ratings, mov[_id]['title'], 500, pearson_correlation)
    return jsonify({'recommendations': data})