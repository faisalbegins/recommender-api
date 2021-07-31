from flask import Flask

import model_initializer
import recommender

app = Flask(__name__)

# initialize all the model during app startup
model_initializer.initialize(app)


# trigger model initialization externally
@app.route('/reload_model')
def reload_models():
    model_initializer.initialize(app)
    return "ok"


@app.route('/trending/score/<int:k>')
@app.route('/trending/score', defaults={'k': 10})
def top_trending_movies(k):
    movies = app.trending_model
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/popularity/<int:k>')
@app.route('/trending/popularity', defaults={'k': 10})
def top_popular_movies(k):
    movies = app.popular_model
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/language/<string:lang>/<int:k>/')
@app.route('/trending/language', defaults={'k': 10, 'lang': 'en'})
def top_movies_by_language(lang, k):
    generic_model = app.generic_model
    movies = recommender.top_movies_by_language(generic_model, lang, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/country/<string:country>/<int:k>/')
@app.route('/trending/country', defaults={'k': 10, 'country': 'US'})
def top_movies_by_country(country, k):
    generic_model = app.generic_model
    movies = recommender.top_movies_by_country(generic_model, country, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/genre/<string:genre>/<int:k>/')
@app.route('/trending/genre', defaults={'k': 10, 'genre': 'Drama'})
def top_movies_by_genre(genre, k):
    generic_model = app.generic_model
    movies = recommender.top_movies_by_genre(generic_model, genre, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/similar/<string:title>/<int:k>')
@app.route('/similar/<string:title>', defaults={'k': 10})
def top_similar_movies(title, k):
    model = app.vectorize_model
    movies = recommender.get_similar_movies(model, title, k)
    movies = [] if movies is None else movies
    return movies.to_json(orient='records')


if __name__ == '__main__':
    app.run()
