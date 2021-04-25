from model.user import User
from extensions import g_redis

class UserRepo:
    def __init__(self):
        pass

    def create_new(self, id):
        user = User(id)
        user.update_to_redis()

    def get_by_id(self, id):
        return User.from_redis(id)

    def remove(self, id):
        g_redis.remove_containing_id(id)
