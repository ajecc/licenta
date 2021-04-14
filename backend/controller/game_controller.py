from model.position import Position
from model.decision import Decision
from model.user import User
from model.card import Card
import time

class GameController:
    # TODO: this needs a method that sorts current players by their position
    def __init__(self, table):
        self._table = table

    def start_game(self):
        while self._have_human_players():
            self._distribute_cards()
            self._process_flop()
            for _ in range(3):
                self._table.add_card()
                self._process_non_flop()
                if self._table.have_no_more_current_players():
                    break
            self._remove_inactive_players()
            self._shift_players_position()
            self._clear()
            self._table.update_to_redis()
            # TODO: update the players as well

    def _process_flop(self):
        # TODO: handle special case: heads-up
        self._find_by_position(Position.SB).bet(self._bb // 2)
        self._table.bet(self._table.bb // 2)
        self._find_by_position(Position.BB).bet(self._bb)
        self._table.bet(self._table.bb)
        utg = self._find_by_position(Position.UTG)
        self._table.current_player_id = utg.id
        self._start_betting_round()

    def _find_by_position(self, position):
        for player in self._table.current_hand_players:
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

    def _process_non_flop(self):
        # TODO: handle heads-up case
        self._table.current_player_id = self.find_by_position_next_or_eq(Position.SB)
        self._start_betting_round()
    
    def _remove_inactive_players(self):
        pass

    def _shift_players_position(self):
        # TODO: handle special cases when some players are inactive
        pass 

    def _start_betting_round(self):
        # TODO: repeat this
        for player in self.table.current_hand_players:
            if player.is_bot:
                # TODO: get decision through DLL call
                decision = Decision.from_json(decision_json)
                pass
            else:
                decision = self.wait_for_decision(player)
                player.signal_processed_decision()
            if decision is None:
                decision = Decision.FOLD
            if decision.bet_ammount is not None:
                if not self._check_bet_ammount(decision.bet_ammount, player):
                    decision = Decision(Decision.CHECK)
            self._alter_on_decision(player, decision)

    def _check_bet_ammount(self, bet_ammount, player):
        if bet_ammount >= player.balance:
            return True
        if bet_ammount < self.table.bb or bet_ammount < 2 * self.talbe.last_bet:
            return False
        return True

    def _add_card(self):
        card = Card.generate_random(self._used_cards)
        self._used_cards.append(card)
        self._cards.append(card)
    
    def _distribute_cards(self):
        pass
    
    def _clear(self):
        pass

    def _alter_on_decision(self, player, decision):
        if decision == Decision.FOLD or (decision == Decision.CHECK and self._table.current_bet > player.current_bet):
            self._table.remove_current_player(player.id)
        elif decision == Decision.CALL:
            decision.bet_ammount = 1 # TODO
        # TODO: this is wrong. Tweak later
        player.balance -= decision.bet_ammount
        player.current_bet = decision.bet_ammount
        self._table.bet(decision.bet_ammount)
            
    def wait_for_decision(self, player):
        poll_tries = 100
        interval = Decision.DECISION_TIME / (poll_tries - 1) 
        for _ in range(poll_tries):
            player = User.from_redis(player.id)
            if player.decision is not None:
                return player.decision
            time.sleep(interval)
        return None

    @staticmethod
    def get_state_json(table_id):
        pass

    @staticmethod
    def get_state_json_for_player(player_id):
        pass

