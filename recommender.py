def top_movies_by_language(df, lang='en', k=10):
    # start processing with a copy of original data
    candidates = df.copy()

    # import dependencies
    from utilities import weighted_rating_supplier

    # get weighted_rating calculator
    weighted_rating = weighted_rating_supplier(df)

    # filter by specific language
    candidates = candidates.loc[df['language'] == lang]
    candidates['score'] = candidates.apply(weighted_rating, axis=1)
    candidates = candidates.sort_values('score', ascending=False)

    # return candidates
    return [] if candidates is None else candidates.head(k)


def top_movies_by_country(df, country='US', k=10):
    # start processing with a copy of original data
    candidates = df.copy()

    # import dependencies
    from ast import literal_eval
    from utilities import to_countries

    # convert json string genres to python boject
    candidates['countries'] = candidates['countries'].apply(literal_eval)
    candidates['countries'] = candidates['countries'].apply(to_countries)

    # Filter movies by specific country
    candidates = candidates[candidates.loc[0:, 'countries'].apply(lambda row: country.upper() in row)]

    # return candidates
    return [] if candidates is None else candidates.head(k)


def top_movies_by_genre(df, genre='Drama', k=10):
    # start processing with a copy of original data
    candidates = df.copy()

    # import dependencies
    from ast import literal_eval
    from utilities import to_genres
    from utilities import weighted_rating_supplier

    # get weighted_rating calculator
    weighted_rating = weighted_rating_supplier(df)

    # convert json string genres to python boject
    candidates['genres'] = candidates['genres'].apply(literal_eval)
    candidates['genres'] = candidates['genres'].apply(to_genres)

    # Filter movies by specific genres
    candidates = candidates[candidates.loc[0:, 'genres'].apply(lambda row: genre.title() in row)]
    candidates['score'] = candidates.apply(weighted_rating, axis=1)
    candidates = candidates.sort_values('score', ascending=False)

    # return candidates
    return [] if candidates is None else candidates.head(k)


def get_similar_movies(df, similarity_matrix, title, k):
    # start processing with a copy of original data
    candidates = df.copy()

    # # Import CountVectorizer and create the count matrix
    # from sklearn.feature_extraction.text import CountVectorizer
    # count = CountVectorizer(stop_words='english')
    # count_matrix = count.fit_transform(candidates['soup'])
    #
    # # Compute the Cosine Similarity matrix based on the count_matrix
    # from sklearn.metrics.pairwise import cosine_similarity
    # cosine_sim = cosine_similarity(count_matrix, count_matrix)

    import pandas as pd
    candidates = candidates.reset_index()
    indices = pd.Series(candidates.index, index=candidates['title'])

    # Get the index of the movie that matches the title
    try:
        idx = indices[title]
    except:
        return candidates[['id','title']].head(k)

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(similarity_matrix[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:k+1]

    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return candidates[['id', 'title']].iloc[movie_indices]


def get_personalized_movies_svd(df, user, k):
    # start processing with a copy of original data
    candidates = df.copy()

    # filter data by user
    candidates = candidates.loc[df['user'] == user]
    if len(candidates.index) == 0:
        return []

    # sort by predicted value
    candidates = candidates.sort_values('prediction', ascending=False)

    # take k number of movies and return
    return candidates.head(k)


def get_prediction_svd(svd, user, movie):
    prediction = svd.predict(user, movie).est
    return str(prediction)


def get_personalized_movies_ncf(app, user, k):
    import numpy as np
    model = app.neural_network
    movie_lens_movies = app.movie_lens_movies
    movie_lens_ratings = app.movie_lens_ratings
    movie_encoder = app.movie_encoder
    movie_decoder = app.movie_decoder
    user_encoder = app.user_encoder
    movies_watched_by_user = movie_lens_ratings[movie_lens_ratings.userId == user]
    movies_not_watched = movie_lens_movies[~movie_lens_movies["movieId"].isin(movies_watched_by_user.movieId.values)]["movieId"]
    movies_not_watched = list(set(movies_not_watched).intersection(set(movie_encoder.keys())))
    movies_not_watched = [[movie_encoder.get(x)] for x in movies_not_watched]
    user_encoder = user_encoder.get(user)
    user_movie_array = np.hstack(([[user_encoder]] * len(movies_not_watched), movies_not_watched))
    ratings = model.predict(user_movie_array).flatten()
    top_ratings_indices = ratings.argsort()[-k:][::-1]
    recommended_movie_ids = [movie_decoder.get(movies_not_watched[x][0]) for x in top_ratings_indices]
    recommended_movies = movie_lens_movies[movie_lens_movies["movieId"].isin(recommended_movie_ids)]
    recommended_movies = recommended_movies[['movieId', 'title']]
    recommended_movies.columns = ['id', 'title']
    return recommended_movies[['id', 'title']]
