"""SIMILARITY CALCULATOR"""

from math import sqrt

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
    for item in prefs[p1]['ratings']:
        if item in prefs[p2]['ratings']:
            similar_items[item] = 1

    #no ratings in common
    if len(similar_items) == 0: return 0

    #square the differences
    sum_of_squares = sum([pow(prefs[p1]['ratings'][item]['rating'] - prefs[p2]['ratings'][item]['rating'], 2) for item in similar_items])

    return 1 / (1 + sqrt(sum_of_squares))

def pearson_correlation(prefs, p1, p2):
    #Get list of mutually rated items
    similar_items = {}
    for item in prefs[p1]['ratings']:
        if item in prefs[p2]['ratings']:
            similar_items[item] = 1

    #number of elements
    n = len(similar_items)

    #No ratings in common
    if n == 0: return 0

    #Add up prefs
    sum1 = sum([prefs[p1]['ratings'][item]['rating'] for item in similar_items])
    sum2 = sum([prefs[p2]['ratings'][item]['rating'] for item in similar_items])

    #Sum squares
    sumsq1 = sum([pow(prefs[p1]['ratings'][item]['rating'], 2) for item in similar_items])
    sumsq2 = sum([pow(prefs[p2]['ratings'][item]['rating'], 2) for item in similar_items])

    #Sum the products
    psum = sum([prefs[p1]['ratings'][item]['rating'] * prefs[p2]['ratings'][item]['rating'] for item in similar_items])

    #calculate pearson score
    num = psum - (sum1 * sum2 / n)
    den = sqrt((sumsq1 - pow(sum1, 2) / n) * (sumsq2 - pow(sum2, 2) / n))
    if den == 0: return 0

    pearson_score = num / den

    return pearson_score

def top_matches(prefs, person, n = 5, similarity = euclidean_distance):

    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    #Sort list highest first
    scores.sort()
    scores.reverse()
    return scores[0:n]

def get_recommendations(prefs, person, similarity):
    totals = {}
    sim_sums = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue
        for item in prefs[other]['ratings']:
            if item not in prefs[person]['ratings'] or prefs[person]['ratings'][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other]['ratings'][item]['rating'] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

        rankings = [(total / sim_sums[item], prefs[other]['ratings'][item]['title']) for item, total in totals.items()]

        rankings.sort()
        rankings.reverse()
        return {'recommendations': rankings}
