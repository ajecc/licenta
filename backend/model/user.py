from extensions import db
from model.elem_bounds import HAND_LEN
from model.board import Board
from model.cred import Cred


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=True)
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

    def join_table(self, table):
        self.table_id = table.id
        User.query.filter_by(id=self.id).update({'table_id': self.table_id})
