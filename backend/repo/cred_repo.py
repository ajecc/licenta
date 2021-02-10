from extensions import db
from model.cred import Cred
from passlib.hash import pbkdf2_sha256

class CredRepo:
    def __init__(self):
        pass

    def add(self, cred):
        db.session.add(cred)
        db.session.commit()

    def contains_username(self, username):
        return Cred.query.filter_by(username=username).first() is not None

    def contains_email(self, email):
        return Cred.query.filter_by(email=email).first() is not None

    def check(self, email, username, password):
        if email is not None:
            return self._check_email_password(email, password)
        if username is not None:
            return self._check_username_password(username, password)
        return False

    def get_by_id(self, id):
        return Cred.query.filter_by(id=id).first()

    def get_by_username(self, username):
        return Cred.query.filter_by(username=username).first()

    def get_by_email(self, email):
        return Cred.query.filter_by(email=email).first()

    def _check_email_password(self, email, password):
        try:
            real_cred = Cred.query.filter_by(email=email).first()
            return pbkdf2_sha256.verify(password, real_cred.password_hash) 
        except Exception as e:
            print(e)
            return False

    def _check_username_password(self, username, password):
        try:
            real_cred = Cred.query.filter_by(username=username).first()
            return pbkdf2_sha256.verify(password, real_cred.password_hash) 
        except Exception as e:
            print(e)
            return False
