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
