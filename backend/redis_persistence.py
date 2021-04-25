from flask_redis import FlaskRedis
import redis
import sys

class RedisPersistence:
    def __init__(self):
        if sys.argv[0] == 'app.py':
            self._redis = FlaskRedis()
        else:
            self._redis = redis.Redis()
    
    def set_raw(self, key, value):
        if value is None:
            self._redis.delete(key)
        else:
            self._redis.set(key, self._convert_set(value))

    def get_raw(self, key):
        return self._convert_get(self._redis.get(key))

    def set(self, id, key, value):
        if value is None:
            self._redis.delete(f'{key}#{id}')
        else:
            value = self._convert_set(value)
            self._redis.set(f'{key}#{id}', value)

    def get(self, id, key):
        value = self._redis.get(f'{key}#{id}')
        return self._convert_get(value)

    def update_list(self, id, key, new_list):
        self._redis.delete(f'{key}#{id}')
        for elem in new_list:
            self._redis.lpush(f'{key}#{id}', self._convert_set(elem))

    def get_list(self, id, key):
        list = self._redis.lrange(f'{key}#{id}', 0, -1)
        return [self._convert_get(elem) for elem in list]

    def exists_key(self, key):
        return self._redis.exists(key)

    def remove_containing_id(self, id):
        for key in self._redis.scan_iter(f'*{id}*'):
            self._redis.delete(key)

    def init_app(self, app):
        self._redis.init_app(app)

    def _convert_get(self, value):
        if value is None:
            return value
        if type(value) is bytes:
            value = value.decode()
        if type(value) is str:
            if value == 'True' or value == 'False':
                return value == 'True'
            if value.isdigit():
                return int(value)
        return value
    
    def _convert_set(self, value):
        if type(value) is bool:
            value = str(value)
        return value
