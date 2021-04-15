from model.card import Card
from extensions import g_redis
import requests
import time


class User:
    @classmethod
    def from_redis(cls, id):
        user = cls(id)
        user._table_id = g_redis.get(id, 'user:table_id')
        user._hand = [Card(g_redis.get(id, 'user:hand_0')), Card(g_redis.get(id, 'user:hand_1'))]
        user._currrent_bet = g_redis.get(id, 'user:current_bet')
        user._balance = g_redis.get(id, 'user:balance')
        return user
        
    def __init__(self, cred_id):
        self._id = cred_id
        self._table_id = None
        self._hand = None
        self._currrent_bet = 0
        self._balance = 0
        self._is_bot = False
        self._position = None
        self._decision = None
        self._is_active = True

    def join_table(self, table):
        self._table_id = table.id
        self.update_to_redis()

    def leave_table(self):
        self._table_id = None
        self.update_to_redis()

    def update_to_redis(self):
        g_redis.set(self._id, 'user:table_id', self._table_id)
        g_redis.set(self._id, 'user:hand_0', str(self._hand[0]))
        g_redis.set(self._id, 'user:hand_1', str(self._hand[1]))
        g_redis.set(self._id, 'user:current_bet', self._currrent_bet)
        g_redis.set(self._id, 'user:balance', self._balance)
    
    def signal_processed_decision(self):
        self._decision = None
        g_redis.set(self._id, 'user:decision', None)

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value):
        self._hand = value

    @property
    def current_bet(self):
        return self._current_bet

    @current_bet.setter
    def current_bet(self, value):
        self._current_bet = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    @property
    def is_bot(self):
        return self._is_bot
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def decision(self):
        return self._decision

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value
