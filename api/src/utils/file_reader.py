"""FILE READER"""

import os
import csv
from flask import current_app

from utils.similarity_calculator import transform_prefs, euclidean_distance, top_matches

DATA_FOLDER = './data'

def read_ratings(filename):
    """Reads the CSV files and builds dict with movie ratings for all users and adds the movie title to the data.

    Returns:
        [dict] -- a Dictionary representing the ratings of all users
    """

    ratings = dict({})
    if filename == 'ratings.csv':
        moviefilename = 'movies.csv'
    elif filename == 'ratingstest.csv':
        moviefilename = 'moviestest.csv'
    movies = read_movies(moviefilename)

    with open(os.path.join(DATA_FOLDER, filename), newline='') as csvfile:
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

def read_movies(filename):
    movies = dict({})
    with open(os.path.join(DATA_FOLDER, filename), newline='') as moviesfile:
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

def read_item_based_data(sim, sim_method, prefs):
    """Reads the CSV files and builds dict with item based collaborative filtering ratings

    Returns:
        [dict] -- a Dictionary representing the item based collaborative filtering
    """

    ratings = dict({})

    filepath = os.path.join(DATA_FOLDER, 'itemratings'+sim+'.csv')

    # Check for file with item based ratings and read
    if os.path.isfile(filepath):
        with open(filepath, newline='') as csvfile:
            ratingsreader = csv.DictReader(csvfile)
            for row in ratingsreader:
                title = row['title']
                other_title = row['otherTitle']
                similarity = float(row['similarity'])
                try:
                    movie = ratings[title]
                except KeyError:
                    movie = dict({})

                movie[other_title] = {
                    'similarity': similarity,
                    'title': other_title
                }
                ratings[title] = movie

    #Write file with item based ratings
    else:
        ratings = calc_similar_items(prefs, filepath, 10, sim_method)

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
        writer.writerow(['title', 'otherTitle', 'similarity'])
        for item in item_prefs:
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
                writer.writerow([item, title, sim_score])

                #Build movie dict for the current user
                try:
                    movie = result[item]
                except KeyError:
                    movie = dict({})

                movie[title] = {
                    'similarity': sim_score,
                    'title': title
                }
                result[item] = movie

    return result
