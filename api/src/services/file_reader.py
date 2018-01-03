import os
import csv
# from models.RecommendationsDB import RecommendationsDB

DATA_FOLDER = './data'

def read_ratings():
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
            except Exception as e:
                user = {'userId': user_id, 'ratings': dict({})}

            title = movies[row['movieId']]['title']
            user['ratings'][row['movieId']] = {
                'movieId': row['movieId'],
                'rating': row['rating'],
                'title': title
            }
            recommendations[user_id] = user

    return recommendations
