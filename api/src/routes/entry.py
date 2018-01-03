"""
Entry route
"""
from flask import Blueprint, jsonify

entry = Blueprint('entry', __name__)


@entry.route('/')
def get_entry():
    """Get list of possible routes"""

    routes = {
        'self': '/',
        'ping': '/ping'
    }

    return jsonify(routes)