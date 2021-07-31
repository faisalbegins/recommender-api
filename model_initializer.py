def initialize(app):
    import constants as const
    import pickle
    with open(const.TRENDING_MODEL, 'rb') as trending_file, \
            open(const.POPULAR_MODEL, 'rb') as popular_file, \
            open(const.GENERIC_MODEL, 'rb') as generic_file, \
            open(const.VECTORIZER_MODEL, 'rb') as vectorize_file:
        app.trending_model = pickle.load(trending_file)
        app.popular_model = pickle.load(popular_file)
        app.generic_model = pickle.load(generic_file)
        app.vectorize_model = pickle.load(vectorize_file)
