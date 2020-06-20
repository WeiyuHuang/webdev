import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def home_run():
        return f"running in home"

    @app.route('/movie', methods=['GET'])
    #@requires_auth('get:movie')
    def get_movies(jwt):
        movies = Movie.query.all()
        if (len(movies) == 0):
            abort(404)

        def movie_json(movie):
            return {
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date
            }

        try:
            movie_list_json = [movie_json(movie) for movie in movies]
            return jsonify({
                'success': True,
                'movies': movie_list_json
            })
        except:
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()