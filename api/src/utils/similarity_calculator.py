"""SIMILARITY CALCULATOR"""

from math import sqrt
from flask import current_app

def euclidean_distance(prefs, p1, p2):
    """Calculates the euclidean distance between 2 people

    Arguments:
        prefs {[type]} -- [description]
        p1 {[type]} -- [description]
        p2 {[type]} -- [description]

    Returns:
        [type] -- [description]
    """


    #Get list of similar items
    similar_items = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            similar_items[item] = 1.0

    #no ratings in common
    if len(similar_items) == 0: return 0

    #square the differences
    sum_of_squares = sum([pow(prefs[p1][item]['rating'] - prefs[p2][item]['rating'], 2) for item in similar_items])

    return 1.0 / (1.0 + sqrt(sum_of_squares))

def pearson_correlation(prefs, p1, p2):
    """Calculates pearson correlation for 2 people

    Arguments:
        prefs {[type]} -- [description]
        p1 {[type]} -- [description]
        p2 {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    #Get list of mutually rated items
    similar_items = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            similar_items[item] = 1.0

    #number of elements
    n = len(similar_items)

    #No ratings in common
    if n == 0:
        return 0

    #Add up prefs
    sum1 = sum([prefs[p1][item]['rating'] for item in similar_items])
    sum2 = sum([prefs[p2][item]['rating'] for item in similar_items])

    #Sum squares
    sumsq1 = sum([pow(prefs[p1][item]['rating'], 2) for item in similar_items])
    sumsq2 = sum([pow(prefs[p2][item]['rating'], 2) for item in similar_items])

    #Sum the products
    psum = sum([prefs[p1][item]['rating'] * prefs[p2][item]['rating'] for item in similar_items])

    #calculate pearson score
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sumsq1 - pow(sum1, 2) / n) * (sumsq2 - pow(sum2, 2) / n))
    if den == 0:
        return 0

    pearson_score = num / den

    return pearson_score

def top_matches(prefs, person, n = 5, similarity = euclidean_distance):
    """Returns n top matches for a person or item

    Arguments:
        prefs {dict} -- ratings dict
        person {string} -- the key to the person/item in the ratings dict

    Keyword Arguments:
        n {int} -- number of matches to return (default: {5})
        similarity {method} -- similarity method to use to find matches (default: {euclidean_distance})
    """

    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    #Sort list highest first
    scores.sort(key=lambda x: x[0])
    scores.reverse()

    return scores[0:n]

def get_recommendations(prefs, person, similarity, n = 20):
    """Gets recommendations for a user based on the given similarity measure (pearson or euclidean)

    Arguments:
        prefs {[type]} -- [description]
        person {int} -- user id of person to get recommendations for
        similarity {method} -- pearson_correlation or euclidean_distance
    """

    totals = {}
    sim_sums = {}

    for other in prefs:
        #Don't compare to self
        if other == person: #or other not in matches:
            continue

        sim = similarity(prefs, person, other)

        #ignore scores of 0 or lower
        if sim <= 0:
            continue

        for item in prefs[other]:

            #only score movies the user hasn't rated
            if item not in prefs[person] or prefs[person][item]['rating'] == 0:
                totals.setdefault(item, 0.0)
                totals[item] += prefs[other][item]['rating'] * sim
                sim_sums.setdefault(item, 0.0)
                sim_sums[item] += sim

    maximum = max(totals.values())
    rankings = [(total / maximum * 5, item) for item, total in totals.items()]

    rankings.sort(key=lambda x: x[0])
    rankings.reverse()
    return {'recommendations': rankings[0:n]}

def transform_prefs(prefs):
    """transforms ratings to be item based"""

    result = {}
    for person in prefs:
        user_id = person
        for item in prefs[person]:
            title = prefs[person][item]['title']
            rating = prefs[person][item]['rating']
            try:
                movie = result[title]
            except KeyError:
                movie = dict({})

            movie[user_id] = {
                'rating': rating,
                'title': title
            }
            result[title] = movie

    return result

def get_recommended_items(prefs, item_match, user):
    """Gets recommended items for a user from item based dataset"""

    user_ratings = prefs[user]
    scores = {}
    total_sim = {}

    #Items rated by the user
    for (item, movie) in user_ratings.items():
        rating = movie['rating']
        #Similar items
        for (item2, movie2) in item_match[item].items():
            if item2 in user_ratings: continue

            similarity = movie2['similarity']

            #Weighted sum of ratings times similarity
            title = movie2['title']
            scores.setdefault(title, 0)
            scores[title] += similarity * rating

            #sum all similarities
            total_sim.setdefault(title, 0)
            total_sim[title] += similarity

    rankings = [(score/total_sim[item], item) for item, score in scores.items() if total_sim[item] != 0]

    rankings.sort(key=lambda x: x[0])
    rankings.reverse()
    return {'recommendations': rankings}
