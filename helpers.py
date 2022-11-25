import random

from models import ShowerThought, Connection, User


def get_random_thought():
    total = ShowerThought.query.count()
    rand = random.randint(0, total)

    thought = ShowerThought.query.get(rand)

    if thought is not None:
        return thought.format()
    else:
        return get_random_thought()


def get_followers(user_id):
    followers_formatted = []

    followers_list = []
    followers_raw = [usr.followers for usr in Connection.query.filter_by(user=user_id).all()]

    try:
        followers_list = followers_raw[0].split(' ')
    except Exception as e:
        raise e
    finally:
        for user in followers_list:
            user_name = (User.query.get(int(user))).name
            followers_formatted.append(user_name)

    return followers_formatted

