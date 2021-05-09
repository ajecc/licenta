import random
import string
from model.elem_bounds import ID_LEN 
from model.card import Card, generate_random
from extensions import g_redis


class Table:
    @classmethod
    def from_redis(cls, id):
        table = cls(id=id)
        table._bots_cnt = g_redis.get(id, 'table:bots_cnt')
        table._current_bet = g_redis.get(id, 'table:current_bet')
        table._pot = g_redis.get(id, 'table:pot')
        table._cards = g_redis.get_list(id, 'table:cards')
        table._cards = [Card(c) for c in table._cards]
        table._current_users_ids = g_redis.get_list(id, 'table:current_users_ids')
        table._current_hand_users_ids = g_redis.get_list(id, 'table:current_hand_users_ids')
        table._used_cards = g_redis.get_list(id, 'table:used_cards')
        table._used_cards = [Card(c) for c in table._used_cards]
        return table

    def __init__(self, bots_cnt=None, id=None):
        if id is None:
            self._id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_LEN))
        else:
            self._id = id
        self._bots_cnt = bots_cnt
        self._pot = 0 
        self._current_bet = 0
        self._cards = []
        self._current_users_ids = []
        self._current_hand_users_ids = []
        self._used_cards = []
        self._bb = 10  # TODO: change me

    def add_user(self, user):
        user.join_table(self)
        self._current_users_ids.append(user.id)
        self.update_to_redis()

    def remove_user(self, user):
        user.leave_table()
        self._current_users_ids = list(filter(lambda id: id != user.id, self._current_users_ids))
        self._current_hand_users_ids = list(filter(lambda id: id != user.id, self._current_hand_users_ids))
        self.update_to_redis()

    def remove_current_hand_user(self, user):
        self._current_hand_users_ids = list(filter(lambda id: id != user.id, self._current_hand_users_ids))
        self.update_to_redis()

    def update_to_redis(self):
        g_redis.set(self._id, 'table:bots_cnt', self._bots_cnt)
        g_redis.set(self._id, 'table:pot', self._pot)
        g_redis.set(self._id, 'table:current_bet', self._current_bet)
        g_redis.update_list(self._id, 'table:cards', [str(card) for card in self._cards])
        g_redis.update_list(self._id, 'table:current_users_ids', self._current_users_ids)
        g_redis.update_list(self._id, 'table:current_hand_users_ids', self._current_hand_users_ids)
        g_redis.update_list(self._id, 'table:used_cards', [str(card) for card in self._used_cards])

    def bet(self, bet, current_bet_user):
        self._pot += bet 
        self._current_bet = max(self._current_bet, current_bet_user)

    def add_card(self):
        self._cards.append(generate_random(self._used_cards))
        self.append_used_card(self._cards[-1])

    def append_used_card(self, card):
        self._used_cards.append(card)

    def clear(self):
        self._pot = 0
        self._current_bet = 0
        self._cards = []
        self._current_hand_users_ids = []
        self._used_cards = []

    @property
    def id(self):
        return self._id

    @property
    def pot(self):
        return self._pot

    @pot.setter
    def pot(self, value):
        self._pot = value

    @property
    def current_bet(self):
        return self._current_bet

    @current_bet.setter
    def current_bet(self, value):
        self._current_bet = value

    @property
    def bb(self):
        return self._bb
    
    @property
    def cards(self):
        return self._cards

    @property
    def current_users_ids(self):
        return self._current_users_ids

    @current_users_ids.setter
    def current_users_ids(self, value):
        self._current_users_ids = value

    @property
    def current_hand_users_ids(self):
        return self._current_hand_users_ids
    
    @current_hand_users_ids.setter
    def current_hand_users_ids(self, value):
        self._current_hand_users_ids = value

    @property
    def used_cards(self):
        return self._used_cards
