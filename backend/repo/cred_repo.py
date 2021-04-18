from model.cred import Cred
from passlib.hash import pbkdf2_sha256
from extensions import g_redis

class CredRepo:
    def __init__(self):
        pass

    def add(self, cred):
        cred.update_to_redis()

    def contains_username(self, username):
        return g_redis.exists_key(f'cred:{username}') 

    def contains_email(self, email):
        return g_redis.exists_key(f'cred:{email}') 

    def check(self, email, username, password):
        if email is not None:
            return self._check_email_password(email, password)
        if username is not None:
            return self._check_username_password(username, password)
        return False

    def get_by_id(self, id):
        return Cred.from_redis(id)

    def get_by_username(self, username):
        return self.get_by_id(g_redis.get_raw(f'cred:{username}'))

    def get_by_email(self, email):
        return self.get_by_id(g_redis.get_raw(f'cred:{email}'))

    def _check_email_password(self, email, password):
        try:
            real_cred = self.get_by_email(email)
            if real_cred is None:
                return False
            return pbkdf2_sha256.verify(password, real_cred.password_hash) 
        except Exception as e:
            print(e)
            return False

    def _check_username_password(self, username, password):
        try:
            real_cred = self.get_by_username(username)
            if real_cred is None:
                return False
            return pbkdf2_sha256.verify(password, real_cred.password_hash) 
        except Exception as e:
            print(e)
            return False
