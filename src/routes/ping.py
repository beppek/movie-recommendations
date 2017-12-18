"""PING"""
from flask import Blueprint, jsonify

ping = Blueprint('ping', __name__)


@ping.route('/ping')
def get_ping():
    """PING"""

    data = {
        'message': 'pong',
        'status': 200
    }

    return jsonify(data)
