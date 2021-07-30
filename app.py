from flask import Flask
import pickle
import constants as const
import service

app = Flask(__name__)


@app.route('/trending/score/<int:k>')
@app.route('/trending/score', defaults={'k': 10})
def top_trending_movies(k):
    infile = open(const.TRENDING_MODEL, 'rb')
    movies = pickle.load(infile)
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/popularity/<int:k>')
@app.route('/trending/popularity', defaults={'k': 10})
def top_popular_movies(k):
    infile = open(const.POPULAR_MODEL, 'rb')
    movies = pickle.load(infile)
    movies = movies.head(k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/language/<string:lang>/<int:k>/')
@app.route('/trending/language', defaults={'k': 10, 'lang': 'en'})
def top_movies_by_language(lang, k):
    infile = open(const.GENERIC_MODEL, 'rb')
    generic_model = pickle.load(infile)
    movies = service.top_movies_by_language(generic_model, lang, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/country/<string:country>/<int:k>/')
@app.route('/trending/country', defaults={'k': 10, 'country': 'US'})
def top_movies_by_country(country, k):
    infile = open(const.GENERIC_MODEL, 'rb')
    generic_model = pickle.load(infile)
    movies = service.top_movies_by_country(generic_model, country, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


@app.route('/trending/genre/<string:genre>/<int:k>/')
@app.route('/trending/genre', defaults={'k': 10, 'genre': 'Drama'})
def top_movies_by_genre(genre, k):
    infile = open(const.GENERIC_MODEL, 'rb')
    generic_model = pickle.load(infile)
    movies = service.top_movies_by_genre(generic_model, genre, k)
    movies = [] if movies is None else movies[['id', 'title']]
    return movies.to_json(orient='records')


if __name__ == '__main__':
    app.run()
