"""FILE READER"""

import os
import csv

DATA_FOLDER = './data'

def read_ratings():
    """Reads the CSV files and builds dict with movie ratings for all users and adds the movie title to the data.

    Returns:
        [dict] -- a Dictionary representing the ratings of all users
    """

    recommendations = dict({})
    movies = dict({})
    with open(os.path.join(DATA_FOLDER, 'movies.csv'), newline='') as moviesfile:
        moviesreader = csv.DictReader(moviesfile)
        for row in moviesreader:
            movies[row['movieId']] = {'title': row['title']}

    with open(os.path.join(DATA_FOLDER, 'ratings.csv'), newline='') as csvfile:
        ratingsreader = csv.DictReader(csvfile)
        for row in ratingsreader:
            user_id = row['userId']
            try:
                user = recommendations[user_id]
            except KeyError:
                user = {'userId': user_id, 'ratings': dict({})}

            title = movies[row['movieId']]['title']
            user['ratings'][row['movieId']] = {
                'movieId': row['movieId'],
                'rating': float(row['rating']),
                'title': title
            }
            recommendations[user_id] = user

    return recommendations

def read_users():
    """Reads the users from the file and returns a list of user ids"""

    users = dict({})
    with open(os.path.join(DATA_FOLDER, 'ratings.csv'), newline='') as csvfile:
        ratingsreader = csv.DictReader(csvfile)
        for row in ratingsreader:
            users[row['userId']] = {'userId': row['userId']}

    return list(users.keys())
