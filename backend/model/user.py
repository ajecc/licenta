from model.card import Card
from model.position import Position
from model.decision import Decision
from model.cred import Cred
from extensions import g_redis
import requests
import json
import time


class User:
    STARTING_BALANCE = 1000

    @classmethod
    def from_redis(cls, id):
        if id is None:
            return None
        user = cls(id)
        user._table_id = g_redis.get(id, 'user:table_id')
        if g_redis.get(id, 'user:hand_0') is not None:
            user._hand = [Card(g_redis.get(id, 'user:hand_0')), Card(g_redis.get(id, 'user:hand_1'))]
        user._current_bet = g_redis.get(id, 'user:current_bet')
        user._balance = g_redis.get(id, 'user:balance')
        user._is_bot = g_redis.get(id, 'user:is_bot')
        user._position = g_redis.get(id, 'user:position')
        if user._position is not None:
            user._position = Position(user._position)
        user._decision = g_redis.get(id, 'user:decision')
        if user._decision is not None:
            user._decision = Decision.from_json(user._decision)
        user._is_active = g_redis.get(id, 'user:is_active')
        user._is_seated = g_redis.get(id, 'user:is_seated')
        user._pl = g_redis.get(id, 'user:pl')
        if user._pl is None:
            user._pl = 0
        else:
            user._pl = int(user._pl)
        return user
        
    def __init__(self, cred_id):
        self._id = cred_id
        self._table_id = None
        self._hand = []
        self._current_bet = 0
        self._balance = User.STARTING_BALANCE 
        self._is_bot = False
        self._position = None
        self._decision = None
        self._is_active = False 
        self._is_seated = True
        self._pl = 0

    def join_table(self, table):
        self._table_id = table.id
        self.update_to_redis()

    def leave_table(self):
        self._table_id = None
        self.update_to_redis()

    def bet(self, bet_size):
        if bet_size > self._balance:
            self._current_bet += self._balance
            temp = self._balance
            self._balance = 0
            return temp
        self._current_bet += bet_size
        self._balance -= bet_size
        return bet_size

    def update_to_redis(self):
        g_redis.set(self._id, 'user:table_id', self._table_id)
        if len(self._hand) != 0:
            g_redis.set(self._id, 'user:hand_0', str(self._hand[0]))
            g_redis.set(self._id, 'user:hand_1', str(self._hand[1]))
        else:
            g_redis.set(self._id, 'user:hand_0', None)
            g_redis.set(self._id, 'user:hand_1', None)
        g_redis.set(self._id, 'user:current_bet', self._current_bet)
        g_redis.set(self._id, 'user:balance', self._balance)
        g_redis.set(self._id, 'user:is_bot', self._is_bot)
        if self._position is not None:
            g_redis.set(self._id, 'user:position', str(self._position))
        else:
            g_redis.set(self._id, 'user:position', None)
        g_redis.set(self._id, 'user:is_active', self._is_active)
        g_redis.set(self._id, 'user:is_seated', self._is_seated)
        g_redis.set(self._id, 'user:pl', self._pl)
    
    def signal_processed_decision(self):
        self._decision = None
        g_redis.set(self._id, 'user:decision', None)

    def take_decision(self, decision):
        self._decision = decision
        g_redis.set(self._id, 'user:decision', decision.to_json())

    def clear(self):
        self._hand = []
        self._current_bet = 0
        self._pl += self._balance - User.STARTING_BALANCE
        self._balance = User.STARTING_BALANCE

    def __str__(self):
        return str(self.__dict__)
    
    @property
    def name(self):
        return Cred.from_redis(self._id).username

    @property
    def pl(self):
        return self._pl

    @pl.setter
    def pl(self, value):
        self._pl = value
    
    @property
    def id(self):
        return self._id

    @property
    def table_id(self):
        return self._table_id

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
    
    @is_bot.setter
    def is_bot(self, value):
        self._is_bot = True
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def decision(self):
        return self._decision

    @decision.setter
    def decision(self, value):
        self._decision = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def is_seated(self):
        return self._is_seated

    @is_seated.setter
    def is_seated(self, value):
        self._is_seated = value
