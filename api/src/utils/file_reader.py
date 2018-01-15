"""FILE READER"""

import os
import csv
from flask import current_app

DATA_FOLDER = './data'

def read_ratings():
    """Reads the CSV files and builds dict with movie ratings for all users and adds the movie title to the data.

    Returns:
        [dict] -- a Dictionary representing the ratings of all users
    """

    ratings = dict({})
    movies = read_movies()

    with open(os.path.join(DATA_FOLDER, 'ratings.csv'), newline='') as csvfile:
        ratingsreader = csv.DictReader(csvfile)
        for row in ratingsreader:
            user_id = row['userId']
            try:
                user = ratings[user_id]
            except KeyError:
                user = dict({})

            title = movies[row['movieId']]['title']
            user[title] = {
                'movieId': row['movieId'],
                'rating': float(row['rating']),
                'title': title
            }
            ratings[user_id] = user

    return ratings

def read_movies():
    movies = dict({})
    with open(os.path.join(DATA_FOLDER, 'movies.csv'), newline='') as moviesfile:
        moviesreader = csv.DictReader(moviesfile)
        for row in moviesreader:
            movies[row['movieId']] = {'title': row['title']}

    return movies

def read_users():
    """Reads the users from the file and returns a list of user ids"""

    users = dict({})
    with open(os.path.join(DATA_FOLDER, 'ratings.csv'), newline='') as csvfile:
        ratingsreader = csv.DictReader(csvfile)
        for row in ratingsreader:
            users[row['userId']] = {'userId': row['userId']}

    return list(users.keys())
