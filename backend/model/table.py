import random
import string
from model.elem_bounds import ID_LEN 
from model.card import Card
from extensions import g_redis


class Table:
    def __init__(self, bots_cnt):
        self._id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_LEN))
        self._bots_cnt = bots_cnt
        self._pot = 0 
        self._current_bet = 0
        self._cards = []
        self._current_users_ids = []
        self._current_hand_users_ids = []
        self._used_cards = []
        self._bb = 100  # TODO: change me

    def add_user(self, user):
        user.join_table(self)
        self._current_users_ids.append(user.id)
        self.update_to_redis()

    def remove_current_hand_user(self, user):
        user.leave_table()
        self._current_hand_users_ids = list(filter(lambda id: id != user.id, self._current_hand_users_ids))
        self.update_to_redis()

    def update_to_redis(self):
        # TODO: update this
        g_redis.set(self._id, 'table:bots_cnt', self._bots_cnt)
        g_redis.set(self._id, 'table:pot', self._pot)
        g_redis.update_list(self._id, 'table:cards', [str(card) for card in self._cards])
        g_redis.set(self._id, 'table:current_user_id', self._current_user_id)
        g_redis.update_list(self._id, 'table:current_users_ids', self._current_users_ids)
        g_redis.update_list(self._id, 'table:current_hand_users_ids', self._current_hand_users_ids)

    def bet(self, bet):
        self.pot += bet
        self.current_bet = bet

    def add_card(self):
        self._cards.append(Card.generate_random(self._used_cards))

    def append_used_card(self, card):
        self._used_cards.append(card)

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
