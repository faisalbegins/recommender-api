def initialize(app):
    import constants as const
    import pickle
    with open(const.TRENDING_DATA, 'rb') as trending_file, \
            open(const.POPULAR_DATA, 'rb') as popular_file, \
            open(const.GENERIC_DATA, 'rb') as generic_file, \
            open(const.CONTENT_BASED_DATA, 'rb') as content_based_file, \
            open(const.SIMILARITY_MATRIX, 'rb') as similarity_file, \
            open(const.PERSONALIZED_SVD_DATA, 'rb') as svd_lookup_file:
        app.trending_data = pickle.load(trending_file)
        app.popular_data = pickle.load(popular_file)
        app.generic_data = pickle.load(generic_file)
        app.content_based_data = pickle.load(content_based_file)
        app.similarity_matrix = pickle.load(similarity_file)
        app.svd_lookup = pickle.load(svd_lookup_file)
