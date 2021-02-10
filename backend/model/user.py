from extensions import db
from model.elem_bounds import HAND_LEN 


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    cred_id = db.Column(db.Integer, db.ForeignKey('cred.id'), nullable=False)
    hand_json = db.Column(db.String(HAND_LEN)) 
    currrent_bet = db.Column(db.Integer) 
    balance = db.Column(db.Integer) 

    def __init__(self, cred_id):
        self.cred_id = cred_id
        self.board_id = None
        self.hand_json = None
        self.currrent_bet = 0
        self.balance = 0
