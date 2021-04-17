from flask_redis import FlaskRedis

class RedisPersistence:
    def __init__(self):
        self._redis = FlaskRedis()
    
    def set_raw(self, key, value):
        if value is None:
            self._redis.delete(key)
        else:
            self._redis.set(key, value)

    def get_raw(self, key):
        return self._redis.get(key)

    def set(self, id, key, value):
        if value is None:
            self._redis.delete(f'{key}#{id}')
        else:
            self._redis.set(f'{key}#{id}', value)

    def get(self, id, key):
        return self._redis.get(f'{key}#{id}')

    def update_list(self, id, key, new_list):
        self._redis.delete(f'{key}#{id}')
        for elem in new_list:
            self._redis.lpush(f'{key}#{id}', elem)

    def get_list(self, id, key):
        return self._redis.lrange(f'{key}#{id}', 0, -1)

    def exists_key(self, key):
        return self._redis.exists(key)

    def remove_containing_id(self, id):
        for key in self._redis.scan_iter(f'*{id}*'):
            self._redis.delete(key)

    def init_app(self, app):
        self._redis.init_app(app)

