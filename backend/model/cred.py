import random
import string
from model.elem_bounds import ID_LEN 
from extensions import g_redis


class Cred:
    @classmethod
    def from_redis(cls, id):
        email = g_redis.get(id, 'cred:email')
        if email is None:
            return None
        username = g_redis.get(id, 'cred:username')
        if username is None:
            return None
        password_hash = g_redis.get(id, 'cred:password_hash')
        if password_hash is None:
            return None
        cred = cls(email, username, password_hash)
        cred._id = id
        return cred

    def __init__(self, email, username, password_hash=None):
        self._id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_LEN))
        self._email = email
        self._username = username 
        if password_hash is None:
            self._password_hash = self._id
        else:
            self._password_hash = password_hash

    def update_to_redis(self):
        g_redis.set(self._id, 'cred:email', self._email)
        g_redis.set(self._id, 'cred:username', self._username)
        g_redis.set(self._id, 'cred:password_hash', self._password_hash)
        g_redis.set_raw(f'cred:{self._email}', self._id)
        g_redis.set_raw(f'cred:{self._username}', self._id)

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def username(self):
        return self._username

    @property
    def password_hash(self):
        return self._password_hash
