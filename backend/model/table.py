from extensions import db
import random
import string
from model.elem_bounds import CARDS_JSON_LEN, CURRENT_PLAYERS_JSON_LEN, CURRENT_HAND_PLAYERS_LEN, UNIQ_CODE_LEN
from sqlalchemy.orm import relationship
from munch import Munch
import json


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    uniq_code = db.Column(db.String(UNIQ_CODE_LEN))
    pot = db.Column(db.Integer)
    cards_json = db.Column(db.String(CARDS_JSON_LEN))
    current_player = db.Column(db.Integer)
    current_players = db.Column(db.String(CURRENT_PLAYERS_JSON_LEN))
    current_hand_players = db.Column(db.String(CURRENT_HAND_PLAYERS_LEN))
    bots_cnt = db.Column(db.Integer)
    users = relationship('User')

    def __init__(self, bots_cnt):
        self.uniq_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(UNIQ_CODE_LEN))
        self.bots_cnt = bots_cnt
        self.pot = 0 
        self.cards = ''
        self.current_player = 0
        self.current_players = '[]'
        self.current_hand_players = '[]'

    def add_user(self, user):
        user.join_table(self)
        current_players_ = self._get_current_players_from_db()
        current_players_.append(user)
        new_current_players = '['
        for current_player, i in enumerate(current_players_):
            new_current_players += json.dumps(current_player)
            if i != len(current_players_) - 1:
                new_current_players += ', '
        new_current_players += ']'
        self.current_players = new_current_players
        Table.query.first(id=self.id).update({'current_players': new_current_players})
        
    def _get_current_players_from_db(self):
        temp = json.loads(self.current_players) 
        current_players_ = []
        for json_ in temp:
            current_players_.append(Munch(json_))
        return current_players_

