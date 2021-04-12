from model.user import User

class UserRepo:
    def __init__(self):
        pass

    def get_by_id(self, id):
        return User.from_redis(id)

