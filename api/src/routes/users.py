"""USERS"""

from flask import Blueprint, jsonify
from services.file_reader import read_ratings, read_users

users = Blueprint('users', __name__)


@users.route('/users')
def get_users():
    """USERS"""

    data = read_users()

    return jsonify(data)
