from model.user import User
from extensions import g_redis

class UserRepo:
    def __init__(self):
        pass

    def get_by_id(self, id):
        return User.from_redis(id)

    def remove(self, id):
        g_redis.remove_containing_id(id)
