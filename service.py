def top_movies_by_language(df, lang='en', k=10):
    c = df['vote_average'].mean()
    m = df['vote_count'].quantile(.9)

    def weighted_rating(x, m=m, c=c):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * c)

    movies_filter_by_language = df.copy().loc[df['language'] == lang]
    movies_filter_by_language['score'] = movies_filter_by_language.apply(weighted_rating, axis=1)
    trending_movies_by_language = movies_filter_by_language.sort_values('score', ascending=False)

    return [] if trending_movies_by_language is None else trending_movies_by_language.head(k)


def top_movies_by_country(df, country='US', k=10):
    from ast import literal_eval

    def to_countries(x):
        if isinstance(x, list):
            names = [i['iso_3166_1'] for i in x]
            return names
        # Return empty list in case of missing/malformed data
        return []

    movies_by_counties = df.copy()
    movies_by_counties['countries'] = movies_by_counties['countries'].apply(literal_eval)
    movies_by_counties['countries'] = movies_by_counties['countries'].apply(to_countries)
    movies_by_counties = movies_by_counties[movies_by_counties.loc[0:, 'countries'].apply(lambda row: country.upper() in row)]

    return [] if movies_by_counties is None else movies_by_counties.head(k)


def top_movies_by_genre(df, genre='Drama', k=10):
    def to_genres(x):
        if isinstance(x, list):
            names = [i['name'] for i in x]
            return names
        # Return empty list in case of missing/malformed data
        return []

    c = df['vote_average'].mean()
    m = df['vote_count'].quantile(.9)

    def weighted_rating(x, m=m, c=c):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * c)

    from ast import literal_eval
    movies_by_genres = df.copy()
    movies_by_genres['genres'] = movies_by_genres['genres'].apply(literal_eval)
    movies_by_genres['genres'] = movies_by_genres['genres'].apply(to_genres)

    # Filter movies by specific genres
    movies_by_genres = movies_by_genres[movies_by_genres.loc[0:, 'genres'].apply(lambda row: genre.title() in row)]
    movies_by_genres['score'] = movies_by_genres.apply(weighted_rating, axis=1)
    movies_by_genres = movies_by_genres.sort_values('score', ascending=False)

    return [] if movies_by_genres is None else movies_by_genres.head(k)


def get_similar_movies(model, title, k):
    title = 'The Dark Knight Rises'
    movies = model.copy()

    print(len(movies.values))

    # Import CountVectorizer and create the count matrix
    from sklearn.feature_extraction.text import CountVectorizer
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(movies['soup'])

    # Compute the Cosine Similarity matrix based on the count_matrix
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    import pandas as pd
    movies = movies.reset_index()
    indices = pd.Series(movies.index, index=movies['title'])

    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return movies['title'].iloc[movie_indices]
