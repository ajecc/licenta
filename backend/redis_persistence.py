from flask_redis import FlaskRedis

class RedisPersistence:
    def __init__(self):
        self._redis = FlaskRedis()
    
    def set_raw(self, key, value):
        self._redis.set(key, value)

    def get_raw(self, key):
        return self._redis.get(key)

    def set(self, id, key, value):
        self._redis.set(f'{key}#{id}', value)

    def get(self, id, key):
        return self._redis.get(f'{key}#{id}')

    def update_list(self, id, key, value):
        self._redis.delete(f'{key}#{id}')
        for elem in value:
            self._redis.lpush(f'{key}#{id}', elem)

    def exists_key(self, key):
        return self._redis.exists(key)

    def init_app(self, app):
        self._redis.init_app(app)

