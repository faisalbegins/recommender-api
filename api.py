import pickle
from recommenders import demographic

infile = open('/Users/Faisal/Development/recommender-storage/model/dr.pickle', 'rb')

demographic_recommender = pickle.load(infile)

print(demographic_recommender.get_recommendation())
