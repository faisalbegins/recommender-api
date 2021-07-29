import pickle
from recommenders import demographic

infile = open('/Users/Faisal/Development/recommender-storage/models/dr.model', 'rb')

weighted_movies = pickle.load(infile)

dr = demographic.DemographicRecommender(weighted_movies)



# print(dr.get_top_trending_movies())
# print('-' * 50)
# print(dr.get_top_popular_movies())

# dr.get_top_movie_based_one_genre()