from repo.user_repo import UserRepo
from model.user import User

class UserController:
    def __init__(self):
        self._repo = UserRepo()

    def create_new(self, cred_id):
        self._repo.create_new(cred_id)

    def get_by_id(self, id):
        return self._repo.get_by_id(id)

    def remove(self, id):
        self._repo.remove(id)
