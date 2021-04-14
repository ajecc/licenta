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
        self._current_player_id = 0
        self._current_players = []
        self._current_hand_players = []
        self._used_cards = []
        self._bb = 100  # TODO: change me
        self._last_bet = 0

    def add_user(self, user):
        user.join_table(self)
        self._current_players.append(user.id)
        self.update_to_redis()

    def remove_user(self, user):
        user.leave_table()
        self._current_players = list(filter(lambda id: id != user.id, self._current_players))
        self.update_to_redis()

    def update_to_redis(self):
        # TODO: update this
        g_redis.set(self._id, 'table:bots_cnt', self._bots_cnt)
        g_redis.set(self._id, 'table:pot', self._pot)
        g_redis.update_list(self._id, 'table:cards', [str(card) for card in self._cards])
        g_redis.set(self._id, 'table:current_player_id', self._current_player_id)
        g_redis.update_list(self._id, 'table:current_players', self._current_players)
        g_redis.update_list(self._id, 'table:current_hand_players', self._current_hand_players)

    def bet(self, bet):
        self.pot += bet
        self.current_bet = bet
