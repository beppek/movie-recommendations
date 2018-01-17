"""FILE READER"""

import os
import csv
from flask import current_app

from utils.similarity_calculator import transform_prefs, euclidean_distance, top_matches

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

def read_item_based_data(similarity, sim_method):
    """Reads the CSV files and builds dict with item based collaborative filtering ratings

    Returns:
        [dict] -- a Dictionary representing the item based collaborative filtering
    """

    ratings = dict({})

    filepath = os.path.join(DATA_FOLDER, 'itemratings'+similarity+'.csv')

    #Check for file with item based ratings and read
    if os.path.isfile(filepath):
        with open(filepath, newline='') as csvfile:
            ratingsreader = csv.DictReader(csvfile)
            for row in ratingsreader:
                title = row['title']
                similarity = float(row['similarity'])
                user_id = row['userId']
                try:
                    movie = ratings[title]
                except KeyError:
                    movie = dict({})

                movie[user_id] = {
                    'similarity': similarity,
                    'title': title
                }
                ratings[title] = movie

    #Write file with item based ratings
    else:
        user_ratings = read_ratings()
        ratings = calc_similar_items(user_ratings, filepath, 10, sim_method)

    return ratings

def calc_similar_items(prefs, filepath, n=10, similarity=euclidean_distance):
    """Calculates item based similarity and writes to csv file
    Arguments:
        prefs {dict} -- dict of ratings

    Keyword Arguments:
        n {int} -- number of recommendations to return (default: {10})
    """

    result = dict({})
    item_prefs = transform_prefs(prefs)
    c = 0
    with open(filepath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'userId', 'otherTitle', 'similarity'])
        for item in item_prefs:
            user_id = list(item_prefs[item].keys())[0]
            c += 1
            # log progress
            if c%100 == 0:
                progress = c/len(item_prefs) * 100
                current_app.logger.debug(str(progress) + '%')

            scores = top_matches(item_prefs, item, n=n, similarity=similarity)
            for score in scores:
                title = score[1]
                sim_score = score[0]

                #Write to file
                writer.writerow([item, user_id, title, sim_score])

                #Build movie dict for the current user
                try:
                    movie = result[title]
                except KeyError:
                    movie = dict({})

                movie[user_id] = {
                    'similarity': sim_score,
                    'title': title
                }
                result[item] = movie

    return result
