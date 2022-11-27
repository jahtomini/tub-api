import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def insert_mock_data():
    db.drop_all()
    db.create_all()
    user_1 = User(name='johncena00034')
    user_2 = User(name='okayletsgooo')
    user_3 = User(name='carefulAstronaut')
    user_4 = User(name='yilongma')
    user_5 = User(name='messi_10')

    shower_thought_1 = ShowerThought(creator='johncena00034', content="It's weird to think that nighttime is the "
                                                                      "natural state of the universe and daytime is "
                                                                      "only caused by a nearby, radiating ball of "
                                                                      "flame.")
    shower_thought_2 = ShowerThought(creator='okayletsgooo', content='A bird can fly but a fly cannot bird.')

    connection_1 = Connection(user=1, followers=None, following='1 3 4')
    connection_2 = Connection(user=3, followers='1 5', following='5 3')

    user_1.insert()
    user_2.insert()
    user_3.insert()
    user_4.insert()
    user_5.insert()

    shower_thought_1.insert()
    shower_thought_2.insert()

    connection_1.insert()
    connection_2.insert()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(24), unique=True)
    showerthoughts = db.relationship("ShowerThought", backref="users", cascade='all, delete')
    connections = db.relationship("Connection", backref="users", cascade='all, delete',)

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User id={self.id}, username={self.name}>'


class ShowerThought(db.Model):
    __tablename__ = 'shower_thoughts'

    id = Column(db.Integer, primary_key=True)
    creator = Column(db.String, db.ForeignKey('users.name'))
    content = Column(db.String(150))

    def __init__(self, creator, content):
        self.creator = creator
        self.content = content

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'creator': self.creator,
            'content': self.content
        }

    def __repr__(self):
        return f'<ShowerThought id={self.id}, creator={self.creator}, content={self.content}>'


class Connection(db.Model):
    __tablename__ = 'connections'

    id = Column(db.Integer, primary_key=True)
    user = Column(db.Integer, db.ForeignKey('users.id'))
    followers = Column(db.String, nullable=True)
    following = Column(db.String, nullable=True)

    def __init__(self, user, followers, following):
        self.user = user
        self.followers = followers
        self.following = following

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user': self.user,
            'followers': self.followers,
            'following': self.following
        }

    def __repr__(self):
        return f'<Connection id={self.id}, user={self.user}, followers={self.followers}, following={self.following}>'
