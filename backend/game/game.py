from model.position import Position
from model.decision import Decision
from model.user import User
from model.card import Card
from model.table import Table
from controller.controllers import user_controller, table_controller
from pokereval.hand_evaluator import HandEvaluator
from game.ai_bridge import AiBridge
import time


class GameHandler:
    def __init__(self, table_id):
        self._table = Table.from_redis(table_id)
        self._current_hand_users = []
        self._current_users = []
        self._ai_bridge = AiBridge()

    def start_game(self):
        while True:
            self._update_current_users()
            if not self._have_human_users():
                break
            self._process_preflop()
            self._process_non_preflop()
            self._decide_winner()
            self._update_current_users()
            self._shift_users_position()
            self._clear()
            self._update_to_redis
            # TODO: update the users as well
        table_controller.remove_table(self._table.id)

    def _have_human_users(self):
        for user in self._current_hand_users:
            if not user.is_bot:
                return True
        return False

    def _update_current_users(self):
        self._table.current_hand_users_ids = []
        new_current_users_ids = []
        for user in self._table._current_users_ids:
            user = User.from_redis(user)
            if user._is_active:
                self._table.current_hand_users_ids.append(user)
                new_current_users_ids.append(user.id)
            else:
                user_controller.remove_user_from_table(user.id)
        self._table.current_users_ids = new_current_users_ids
        # TODO: check if we can do it like this 
        # (having different objects for current_user and current_hand_users)
        self._current_users = [User.from_redis(id) for id in self._table.current_users_ids]
        self._current_hand_users = [User.from_redis(id) for id in self._table.current_hand_users_ids]

    def _process_preflop(self):
        self._distribute_cards()
        self._find_by_position(Position(*Position.SB)).bet(self._table.bb // 2)
        self._table.bet(self._table.bb // 2)
        self._find_by_position(Position(*Position.BB)).bet(self._table.bb)
        self._table.bet(self._table.bb)
        # TODO: handle special case: heads-up
        self._sort_current_hand_users_by_pos(Position(*Position.UTG))
        self._start_betting_round()

    def _find_by_position(self, position):
        for user in self._current_hand_users:
            if user.position == position:
                return user
        return None

    def _process_non_preflop(self):
        # TODO: handle heads-up case
        self._sort_current_hand_users_by_pos(Position(*Position.SB))
        for round_ind in range(3):
            self._table.add_card()
            if round_ind == 0:
                self._table.add_card()
                self._table.add_card()
            self._start_betting_round()
            if self._table.have_no_more_current_users():
                break

    def _shift_users_position(self):
        new_current_users = []
        for user in self._current_users:
            user.position = user.position.get_next()
            new_current_users.append(user)
        self._current_users = new_current_users

    def _start_betting_round(self):
        # TODO: repeat this
        for user in self._current_hand_users:
            if user.is_bot:
                decision = self._ai_bridge.get_decision(self.to_json_for_user(user.id))
            else:
                decision = self.wait_for_decision(user)
                user.signal_processed_decision()
            if decision is None:
                decision = Decision.FOLD
                user.is_active = False
            if decision.bet_ammount is not None:
                if not self._check_bet_ammount(decision.bet_ammount, user):
                    decision = Decision(Decision.CHECK)
            self._alter_on_decision(user, decision)
        self._update_to_redis()

    def _check_bet_ammount(self, bet_ammount, user):
        if bet_ammount == user.balance:
            return True
        if bet_ammount > user.balance:
            return False 
        if bet_ammount < self.table.bb or bet_ammount < 2 * self.talbe.current_bet:
            return False
        return True

    def _add_card(self):
        card = Card.generate_random(self._used_cards)
        self._used_cards.append(card)
        self._cards.append(card)
    
    def _distribute_cards(self):
        for user in self._current_hand_users:
            card_0 = Card.generate_random(self._table.used_cards)
            self._table.append_user_card(card_0)
            card_1 = Card.generate_random(self._table.used_cards)
            self._table.append_used_card(card_1)
            user.hand = [card_0, card_1]

    def _decide_winner(self):
        board = [c.to_pokereval() for c in self._table.cards]
        winner = None
        max_score = -1
        for user in self._current_hand_users:
            hole = [c.to_pokereval() for c in user.hand]
            score = HandEvaluator.evaluate_hand(hole, board)
            if score > max_score:
                winner = user
                max_score = score
        winner.balance += self._table.pot

    def _sort_current_hand_users_by_pos(self, start_pos):
        self._current_hand_users = sorted(self._current_hand_users,
                lambda u: u.position.index if u.position.index >= start_pos.index else Position(*Position.UTG_2).index + 1 + u.position.index) 

    def _clear(self):
        for user in self._current_users:
            user.clear()
        self._table.clear()

    def _update_to_redis(self):
        for user in self._current_users:
            user.update_to_redis()
        self._table.update_to_redis()
    
    def _alter_on_decision(self, user, decision):
        if decision == Decision.FOLD or (decision == Decision.CHECK and self._table.current_bet > user.current_bet and user.current_bet != user.balance):
            self._table.remove_current_hand_user(user.id)
            self._current_hand_users_ids = list(filter(lambda u: u.id != user.id, self._current_hand_users_ids))
        elif decision == Decision.CALL:
            decision.bet_ammount = 1 # TODO
        # TODO: this is wrong. Tweak later
        user.balance -= decision.bet_ammount
        user.current_bet = decision.bet_ammount
        self._table.bet(decision.bet_ammount)
            
    def wait_for_decision(self, user):
        if user.balance == 0:
            return Decision.CHECK
        poll_tries = 100
        interval = Decision.DECISION_TIME / (poll_tries - 1) 
        for _ in range(poll_tries):
            user = User.from_redis(user.id)
            if user.decision is not None:
                return user.decision
            time.sleep(interval)
        return None

    def to_json_for_user(self, user_id):
        # TODO: this
        pass
