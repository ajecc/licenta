import random
import string
from model.elem_bounds import ID_LEN 
from model.position import Position
from model.decision import Decision
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

    def start_game(self):
        while self._have_human_players():
            self._distribute_cards()
            self._process_flop()
            for _ in range(3):
                self._add_card()
                self._process_non_flop()
                if len(self._current_hand_players) <= 1:
                    break
            self._remove_inactive_players()
            self._shift_players_position()
            self._clear()
            self.update_to_redis()
            # TODO: update the players as well

    def _have_human_players(self):
        return True
    
    def _process_flop(self):
        # TODO: handle special case: heads-up
        self._find_by_position(Position.SB).bet(self._bb // 2)
        self._find_by_position(Position.BB).bet(self._bb)
        self._pot += self._bb + self._bb // 2
        self._current_bet = self._bb
        utg = self._find_by_position(Position.UTG)
        self._current_player_id = utg.id
        self._start_betting_round()

    def _process_non_flop(self):
        # TODO: handle heads-up case
        self._current_player_id = self._find_by_position_next_or_eq(Position.SB)
        self._start_betting_round()
    
    def _find_by_position(self, position):
        for player in self._current_hand_players:
            if player.position == position:
                # TODO: I have the id here. Get the player from redis
                return player
        return None

    def _find_by_position_next_or_eq(self, position):
        for _ in range(6):
            player = self._find_by_position(position)
            if player is not None:
                return player
            position = position.get_next()
        raise ValueError('Could not find next position')
        
    def _remove_inactive_players(self):
        pass

    def _shift_players_position(self):
        # TODO: handle special cases when some players are inactive
        pass 

    def _start_betting_round(self):
        for player in self._current_hand_players:
            if player.is_bot:
                # TODO: get decision through DLL call
                pass
            else:
                decision_json = player.wait_for_decision()
            # TODO: create Decision class
            try:
                decision = Decision.from_json(decision_json)
                if decision.bet_ammount is not None:
                    # TODO: sanitize bet ammount
                    pass
            except:
                # TODO: log decision error or communicate to player
                pass


    def _add_card(self):
        card = Card.generate_random(self._used_cards)
        self._used_cards.append(card)
        self._cards.append(card)
    
    def _distribute_cards(self):
        pass
    
    def _send_state_to_players(self):
        state_json = self._get_state_json()
        for player in self._current_hand_players:
            if not player.is_bot:
                # TODO: add this method to player class
                player.send_table_state(state_json)
    
    def _clear(self):
        pass
