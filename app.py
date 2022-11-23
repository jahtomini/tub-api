import os
import random
from flask import Flask, jsonify
from models import setup_db, User, ShowerThought, Connection, insert_mock_data
from flask_cors import CORS

'''
--------------- UTILITY FUNCTIONS 
'''


def get_random_thought():
    total = ShowerThought.query.count()
    rand = random.randint(0, total)

    thought = ShowerThought.query.get(rand)

    if thought is not None:
        return thought.format()
    elif thought is None:
        return get_random_thought()


def get_followers(user_id):
    followers_formatted = []

    users = []
    followers_raw = [usr.followers for usr in Connection.query.filter_by(user=user_id).all()]

    try:
        users = followers_raw[0].split(' ')
    except:
        return followers_formatted
    finally:
        for user in users:
            user_name = (User.query.get(int(user))).name
            followers_formatted.append(user_name)

    return followers_formatted


'''
--------------- APP
'''


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({
            "hello": "Welcome to the Tub API! Consult the documentation to get started.",
            "message": "The Tub API is the core backend for the nonexistent Tub platform where users can share "
                       "shower thoughts with each other."
        })

    # TODO: ensure this is authenticated w/ permissions & is turned into a POST request
    @app.route('/reset_db', methods=['GET'])
    def reset_db():
        insert_mock_data()
        return jsonify({
            "message": "Database has been reset."
        })

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        shower_thoughts = ShowerThought.query.filter_by(creator=user.name).all()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "shower_thoughts": [thought.format() for thought in shower_thoughts]
        })

    @app.route('/users/<int:user_id>/followers', methods=['GET'])
    def get_user_followers(user_id):
        user = User.query.get(user_id)

        return jsonify({
            "id": user.id,
            "username": user.name,
            "followers": get_followers(user_id)
        })

    @app.route('/random', methods=['GET'])
    def get_random_shower_thought():
        return get_random_thought()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001)
