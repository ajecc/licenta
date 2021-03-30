import flask
import os
from extensions import db
from flask_session import Session

# routes
from routes.auth import auth
from routes.empty import empty

app = flask.Flask(__name__)

SECRET_KEY = b'CHANGE THIS'
SQLALCHEMY_DATABASE_URI = 'sqlite:///poker.db' 
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


def register_extensions():
    db.init_app(app)


def register_blueprints():
    app.register_blueprint(auth)
    app.register_blueprint(empty)


def db_create_all():
    register_extensions()
    import model.board
    import model.cred
    import model.user
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    register_blueprints()
    register_extensions()
    app.run()

