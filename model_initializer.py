def initialize(app):
    import constants as const
    import pickle
    with open(const.TRENDING_DATA, 'rb') as trending_file, \
            open(const.POPULAR_DATA, 'rb') as popular_file, \
            open(const.GENERIC_DATA, 'rb') as generic_file, \
            open(const.CONTENT_BASED_DATA, 'rb') as content_based_file, \
            open(const.SIMILARITY_MATRIX, 'rb') as similarity_file, \
            open(const.PERSONALIZED_SVD_RAW, 'rb') as svd_raw_file, \
            open(const.PERSONALIZED_SVD_DATA, 'rb') as svd_lookup_file, \
            open(const.MOVIE_LENS_RATINGS_DATA, 'rb') as movie_lens_ratings_file, \
            open(const.MOVIE_LENS_MOVIES_DATA, 'rb') as movie_lens_movie_lens_file, \
            open(const.MOVIE_ENCODER, 'rb') as movie_encoder_file, \
            open(const.MOVIE_DECODER, 'rb') as movie_decoder_file, \
            open(const.USER_ENCODER, 'rb') as user_encoder_file:
        app.trending_data = pickle.load(trending_file)
        app.popular_data = pickle.load(popular_file)
        app.generic_data = pickle.load(generic_file)
        app.content_based_data = pickle.load(content_based_file)
        app.similarity_matrix = pickle.load(similarity_file)
        app.svd_raw = pickle.load(svd_raw_file)
        app.svd_lookup = pickle.load(svd_lookup_file)
        app.movie_lens_ratings = pickle.load(movie_lens_ratings_file)
        app.movie_lens_movies = pickle.load(movie_lens_movie_lens_file)
        app.movie_encoder = pickle.load(movie_encoder_file)
        app.movie_decoder = pickle.load(movie_decoder_file)
        app.user_encoder = pickle.load(user_encoder_file)

    import tensorflow as tf
    app.neural_network = tf.keras.models.load_model(const.PERSONALIZED_NCF_MODEL_DIR)
