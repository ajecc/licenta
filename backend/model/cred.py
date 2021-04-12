import random
import string
from model.elem_bounds import ID_LEN 
from extensions import g_redis


class Cred:
    @classmethod
    def from_redis(cls, id):
        email = g_redis.get(id, 'cred:email')
        username = g_redis.get(id, 'cred:username')
        password_hash = g_redis.get(id, 'cred:password_hash')
        cred = cls(email, username, password_hash)
        cred._id = id
        return cred

    def __init__(self, email, username, password_hash):
        self._id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_LEN))
        self._email = email
        self._username = username 
        self._password_hash = password_hash

    def update_to_redis(self):
        g_redis.set(id, 'cred:email', self._email)
        g_redis.set(id, 'cred:username', self._username)
        g_redis.set(id, 'cred:password_hash', self._password_hash)
        g_redis.set_raw(f'cred:{self._email}', id)
        g_redis.set_raw(f'cred:{self._username}', id)

    @property
    def id(self):
        return self._id
