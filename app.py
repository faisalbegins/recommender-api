from flask import Flask, render_template

import model_initializer
import recommender

app = Flask(__name__)

# initialize all the model during app startup
model_initializer.initialize(app)


@app.route('/')
def index():
    return render_template('index.html')


# trigger model initialization externally
@app.route('/reload_model')
def reload_models():
    model_initializer.initialize(app)
    return "ok"


@app.route('/trending/score/<int:k>')
@app.route('/trending/score', defaults={'k': 10})
def top_trending_movies(k):
    movies = app.trending_data
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/popularity/<int:k>')
@app.route('/trending/popularity', defaults={'k': 10})
def top_popular_movies(k):
    movies = app.popular_data
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/language/<string:lang>/<int:k>/')
@app.route('/trending/language/<string:lang>', defaults={'k': 10})
@app.route('/trending/language', defaults={'k': 10, 'lang': 'en'})
def top_movies_by_language(lang, k):
    movies = recommender.top_movies_by_language(app.generic_data, lang, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/country/<string:country>/<int:k>/')
@app.route('/trending/country/<string:country>', defaults={'k': 10})
@app.route('/trending/country', defaults={'k': 10, 'country': 'US'})
def top_movies_by_country(country, k):
    movies = recommender.top_movies_by_country(app.generic_data, country, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/genre/<string:genre>/<int:k>/')
@app.route('/trending/genre/<string:genre>', defaults={'k': 10})
@app.route('/trending/genre', defaults={'k': 10, 'genre': 'Drama'})
def top_movies_by_genre(genre, k):
    movies = recommender.top_movies_by_genre(app.generic_data, genre, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/similar/<string:title>/<int:k>')
@app.route('/similar/<string:title>', defaults={'k': 10})
def top_similar_movies(title, k):
    movies = recommender.get_similar_movies(app.content_based_data, app.similarity_matrix, title, k)
    movies = [] if movies is None else movies
    return movies.to_json(orient='records')


@app.route('/personalized/svd/<int:user>/<int:k>')
@app.route('/personalized/svd/<int:user>', defaults={'k': 5})
def top_personalized_movies_svd(user, k):
    movies = recommender.get_personalized_movies_svd(app.svd_lookup, user, k)
    movies = [] if movies is None else movies
    return movies.to_json(orient='records')


@app.route('/personalized/svd/raw/<int:user>/<int:movie>')
def predict_rating(user, movie):
    return recommender.get_prediction_svd(app.svd_raw, user, movie)


@app.route('/personalized/ncf/<int:user>/<int:k>')
@app.route('/personalized/ncf/<int:user>', defaults={'k': 10})
def top_personalized_movies_ncf(user, k):
    movies = recommender.get_personalized_movies_ncf(app, user, k)
    movies = [] if movies is None else movies
    return movies.to_json(orient='records')


if __name__ == '__main__':
    app.run()
