class DemographicRecommender:
    def __init__(self, weighted_movies):
        self.weighted_movies = weighted_movies

    def get_top_trending_movies(self, k=10):
        qualified_movies = self.weighted_movies.sort_values('score', ascending=False)
        return qualified_movies[['title', 'vote_count', 'vote_average', 'score']].head(k)

    def get_top_popular_movies(self, k=10):
        qualified_movies = self.weighted_movies.sort_values('popularity', ascending=False)
        return qualified_movies[['title', 'vote_count', 'vote_average', 'popularity']].head(k)

    def get_top_movie_based_one_genre(self, k=10, genre=None):
        qualified_movies = self.weighted_movies.sort_values('score', ascending=False).head(k)

        print(type(qualified_movies))

        print(qualified_movies.loc[0:1])

        # count = 0
        # for row in qualified_movies.values:
        #     if count == 5:
        #         break
        #     print(row[0:1])
        #     count += 1

