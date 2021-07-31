def weighted_rating_supplier(df):
    c = df['vote_average'].mean()
    m = df['vote_count'].quantile(.9)

    def weighted_rating(x, m=m, c=c):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * c)

    return weighted_rating


def to_countries(x):
    if isinstance(x, list):
        names = [i['iso_3166_1'] for i in x]
        return names
    # Return empty list in case of missing/malformed data
    return []


def to_genres(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        return names
    # Return empty list in case of missing/malformed data
    return []