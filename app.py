import os
import sys

from flask import Flask, jsonify, abort, request

from models import setup_db, User, ShowerThought, insert_mock_data
from helpers import get_random_thought, get_followers
from auth import requires_auth, AuthError

from flask_cors import CORS

PORT = os.environ["PORT"]

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return "Welcome to the Tub API, the core backend for the nonexistent Tub platform where users can " \
               "share shower thoughts with each other."

    @app.route('/db', methods=['DELETE'])
    @requires_auth(permission='delete:user')
    def reset_db(payload):
        insert_mock_data()
        return jsonify({
            "message": "Database has been reset."
        }), 200

    @app.route('/all')
    def get_all_shower_thoughts():
        all_shower_thoughts = [thought.format() for thought in
                               ShowerThought.query.order_by(ShowerThought.creator).all()]
        return jsonify(all_shower_thoughts)

    @app.route('/random', methods=['GET'])
    def get_random_shower_thought():
        return jsonify({
            "random": get_random_thought()
        })

    @app.route('/shower_thoughts', methods=['POST'])
    @requires_auth(permission='add:showerthought')
    def add_new_shower_thought(payload):
        data = request.get_json()
        error = None

        creator_exists = False

        users = User.query.all()

        for user in users:
            if data["creator"] != user.name:
                continue
            else:
                creator_exists = True

        if data and (creator_exists is True):
            try:
                all_of_em = ShowerThought.query.all()
                for x in all_of_em:
                    if x.creator == data["creator"] and x.content == data["content"]:
                        error = 1
                        return error

                new_shower_thought = ShowerThought(creator=data["creator"], content=data["content"])
                new_shower_thought.insert()
            except Exception as e:
                print(sys.exc_info())
                print(e)
            finally:
                if error == 1:
                    return jsonify({
                        "success": False,
                        "message": "Identical showerthought already exists"
                    }), 400
                elif error is None:
                    return jsonify({
                        "success": True,
                        "message": "New showerthought created",
                        "status": 201,
                        "creator": data["creator"],
                        "content": data["content"],
                    }), 201
        else:
            abort(400)

    @app.route('/shower_thoughts/<int:item_id>', methods=['PATCH'])
    @requires_auth(permission='edit:showerthought')
    def edit_shower_thought(payload, item_id):
        shower_thought = ShowerThought.query.get(item_id)
        data = request.get_json()
        print(data)
        error = None

        try:
            the_id = shower_thought.id
            print(the_id)
            shower_thought.content = data["content"]
            shower_thought.update()
        except Exception as e:
            print(sys.exc_info(), e)
            error = 1
        finally:
            if error is None:
                return jsonify({
                    "success": True,
                    "content": shower_thought.content,
                    "by": shower_thought.creator
                }), 200
            else:
                abort(404)

    @app.route('/shower_thoughts/<int:item_id>', methods=['DELETE'])
    @requires_auth(permission='delete:showerthought')
    def delete_shower_thought(payload, item_id):
        error = None
        try:
            item = ShowerThought.query.get(item_id)
            item.delete()
        except Exception as e:
            error = 1
            print(e)
            print(sys.exc_info())
        finally:
            if error is None:
                return jsonify({
                    "message": "Showerthought successfully deleted.",
                    "id": item_id,
                }), 200
            else:
                abort(404)

    @app.route('/users', methods=['POST'])
    @requires_auth(permission='add:user')
    def add_new_user(payload):
        new_user = None
        data = request.get_json()
        error = None

        try:
            existing_users = User.query.all()
            for user in existing_users:
                if user.name == data["name"]:
                    error = 1

            new_user = User(name=data["name"])
            new_user.insert()
        except Exception as e:
            print(sys.exc_info())
            print(e)
        finally:
            if error == 1:
                return jsonify({
                    "success": False,
                    "message": "User with that name already exists"
                }), 400
            elif error is None:
                return jsonify({
                    "success": True,
                    "message": "New user created",
                    "status": 201,
                    "user_id": new_user.id,
                    "user_name": new_user.name
                }), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    @requires_auth(permission='get:user')
    def get_user(payload, user_id):
        error = False
        user = User.query.get(user_id)

        try:
            shower_thoughts = ShowerThought.query.filter_by(creator=user.name).all()
        except:
            error = True
        finally:
            if error is True:
                abort(404)
            else:
                return jsonify({
                    "id": user.id,
                    "name": user.name,
                    "shower_thoughts": [thought.format() for thought in shower_thoughts]
                }), 200

    @app.route('/users/<int:user_id>/followers', methods=['GET'])
    @requires_auth(permission='get:user')
    def get_user_followers(payload, user_id):
        error = 0
        user = User.query.get(user_id)
        followers = None

        try:
            followers = get_followers(user_id)
            return jsonify({
                "success": True,
                "user_id": user.id,
                "username": user.name,
                "followers": followers
            }), 200
        except Exception as e:
            print(e)
            print(sys.exc_info())
        finally:
            if user is None:
                print(str(error))
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "This user does not exist.",
                }), 404
            else:
                return jsonify({
                    "success": True,
                    "user_id": user.id,
                    "username": user.name,
                    "followers": followers
                }), 200

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @requires_auth(permission='delete:user')
    def delete_user(payload, user_id):
        error = None
        try:
            user = User.query.get(user_id)
            print(user)
            user.delete()
        except Exception as e:
            error = 1
            print(e)
            print(sys.exc_info())
        finally:
            if error is None:
                return jsonify({
                    "message": "User account successfully deleted.",
                    "id": user_id,
                }), 200
            else:
                abort(404)

    @app.route('/users', methods=['GET'])
    @requires_auth(permission='get:user')
    def get_all_users(payload):
        raw_users = User.query.order_by(User.id).all()
        users = []

        try:
            for user in raw_users:
                user_followers, user_data = None, None
                try:
                    user_data = user.format()
                    user_followers = get_followers(user.id)
                except Exception as e:
                    print(e)
                finally:
                    data = {
                        "user": user_data,
                        "followers": user_followers
                    }
                    users.append(data)
        except Exception as e:
            print(e)
        finally:
            return jsonify({
                "users": users,
            })

    '''
    --------------- ERROR CODES
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request."
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized."
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden."
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed."
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity."
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        print(error.status_code)
        if error.status_code == 401:
            return jsonify({
                "success": False,
                "error": 401,
                "message": "unauthorized"
            }), 401
        elif error.status_code == 403:
            return jsonify({
                "success": False,
                "error": 403,
                "message": "forbidden"
            }), 403
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT or 3001)
