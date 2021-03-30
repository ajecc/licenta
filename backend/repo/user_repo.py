from extensions import db
from model.user import User

class UserRepo:
    def __init__(self):
        pass

    def create_new(self, cred_id):
        db.session.add(User(cred_id))
        db.session.commit()

    def get_by_id(self, id):
        return User.query.filter_by(id=id).first()

