from repo.user_repo import UserRepo
from model.user import User

class UserController:
    def __init__(self):
        self.repo = UserRepo()

    def create_new(self, cred_id):
        self.repo.create_new(cred_id)
