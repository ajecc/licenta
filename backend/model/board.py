from extensions import db
from model.elem_bounds import CARDS_JSON_LEN, CURRENT_PLAYERS_JSON_LEN, CURRENT_HAND_PLAYERS_LEN
from sqlalchemy.orm import relationship


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    pot = db.Column(db.Integer)
    cards_json = db.Column(db.String(CARDS_JSON_LEN))
    current_player = db.Column(db.Integer)
    users = relationship('User')

    def __init__(self, id, pot, cards_json, current_player, players):
        self.id = id
        self.pot = pot
        self.cards = cards_json  # TODO
        self.current_player = current_player 
        self.players = players
