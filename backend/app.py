import flask
import os
from extensions import g_redis
from flask_session import Session

# routes
from routes.auth import auth
from routes.empty import empty

app = flask.Flask(__name__)

SECRET_KEY = b'CHANGE THIS'
SESSION_TYPE = 'filesystem'
REDIS_URL = 'redis://localhost:6379/0'
app.config.from_object(__name__)
Session(app)


def register_extensions():
    g_redis.init_app(app)


def register_blueprints():
    app.register_blueprint(auth)
    app.register_blueprint(empty)


if __name__ == '__main__':
    register_blueprints()
    register_extensions()
    app.run()

