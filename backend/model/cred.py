from extensions import db
from model.elem_bounds import EMAIL_LEN, USERNAME_LEN, PASSWORD_HASH_LEN
from sqlalchemy.orm import relationship


class Cred(db.Model):
    __tablename__ = 'cred'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(EMAIL_LEN), unique=True, nullable=False)
    username = db.Column(db.String(USERNAME_LEN), unique=True, nullable=False) 
    password_hash = db.Column(db.String(PASSWORD_HASH_LEN))
    user = relationship('User')

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username 
        self.password_hash = password_hash
