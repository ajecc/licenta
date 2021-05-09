from model.position import Position
from model.decision import Decision
from model.user import User
from model.card import Card, generate_random
from model.table import Table
from model.cred import Cred
from controller.controllers import user_controller, table_controller
from pokereval.hand_evaluator import HandEvaluator
from game.ai_bridge import AiBridge
from extensions import g_redis
import sys
import time
import copy
import json
import time


class GameHandler:
    def __init__(self, table_id):
        self._table = Table.from_redis(table_id)
        self._current_hand_users = []
        self._current_users = []
        self._ai_bridge = AiBridge()
        self._cards_visible = False
        self._to_remove = []

    def start_game(self):
        self._seat_users()
        self._assign_positions()
        while True:
            print('updating current users')
            self._update_current_users()
            for user in self._current_hand_users:
                print(user)
            if not self._have_human_users():
                break
            print('have humans')
            print('processing preflop')
            self._process_preflop()
            print('processing nonpreflop')
            self._process_non_preflop()
            print('deciding winner')
            self._decide_winner()
            self._cards_visible = True
            self._update_to_redis()
            print('sleeping a bit')
            time.sleep(5)
            self._cards_visible = False
            print('updating users')
            self._update_current_users()
            print('shifting positions')
            self._shift_users_position()
            print('clearing')
            self._clear()
            print('updating to redis')
            self._update_to_redis()
        table_controller.remove_table(self._table.id)
        time.sleep(60)
        sys.exit()

    def _have_human_users(self):
        for user in self._current_hand_users:
            if not user.is_bot:
                return True
        return False

    def _assign_positions(self):
        self._current_users = [User.from_redis(id) for id in self._table.current_users_ids]
        for i, _ in enumerate(self._current_users):
            self._current_users[i].position = Position(index=len(self._current_users) - i - 1)
            self._current_users[i].update_to_redis()

    def _seat_users(self):
        self._current_users = [User.from_redis(id) for id in self._table.current_users_ids]
        for i, _ in enumerate(self._current_users):
            self._current_users[i].is_seated = True
            self._current_users[i].update_to_redis()

    def _update_current_users(self):
        self._table.current_users_ids = Table.from_redis(self._table.id).current_users_ids
        self._table.current_hand_users_ids = []
        new_current_users_ids = []
        for id in self._table.current_users_ids:
            user = User.from_redis(id)
            print('got user')
            if user.is_seated:
                self._table.current_hand_users_ids.append(user.id)
                new_current_users_ids.append(user.id)
            elif user.is_bot:
                table_controller.remove_user_from_table(user)
                user_controller.remove(user.id)
            else:
                table_controller.remove_user_from_table(user)
        self._table.current_users_ids = new_current_users_ids
        self._current_users = [User.from_redis(id) for id in self._table.current_users_ids]
        self._current_hand_users = []
        for i, _ in enumerate(self._current_users):
            self._current_hand_users.append(self._current_users[i])

    def _process_preflop(self):
        self._distribute_cards()
        bet = self._find_by_position(Position(*Position.SB)).bet(self._table.bb // 2)
        self._table.bet(bet, bet)
        bet = self._find_by_position(Position(*Position.BB)).bet(self._table.bb)
        self._table.bet(bet, bet)
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
            if len(self._current_hand_users) <= 1:
                break
            self._table.add_card()
            if round_ind == 0:
                self._table.add_card()
                self._table.add_card()
            self._table.current_bet = 0
            for i, _ in enumerate(self._current_users):
                self._current_users[i].current_bet = 0
            time_ = time.time()
            self._start_betting_round()
            time_diff = time.time() - time_
            if time_diff < 2:
                time.sleep(2 - time_diff)

    def _shift_users_position(self):
        # TODO: handle heads-up
        for i, user in enumerate(self._current_users):
            if user.position == Position.D:
                dealer_idx = i
                break
        current_position_index = 0
        for i in range(dealer_idx - 1, -1, -1):
            self._current_users[i].position = Position(index=current_position_index)
            current_position_index += 1
        for i in range(len(self._current_users) - 1, dealer_idx - 1, -1):
            self._current_users[i].position = Position(index=current_position_index)
            current_position_index += 1

    def _start_betting_round(self):
        # TODO: last player can still bet (even though he should't)
        # TODO: on all ins, just skip players
        continue_betting = True
        while continue_betting:
            self._to_remove = []
            for i, _ in enumerate(self._current_hand_users):
                print(f'Current player position is: {self._current_hand_users[i].position.position}')
                if len(self._to_remove) == len(self._current_hand_users) - 1:
                    break
                if not self._can_take_action(self._current_hand_users[i]):
                    continue
                decision_time = None
                self._current_hand_users[i].is_active = True
                if self._current_hand_users[i].is_bot:
                    print('Getting decision from bot')
                    decision_time = time.time()
                    decision = self._ai_bridge.get_decision(self.to_json_for_user(self._current_hand_users[i].id))
                    decision_time = time.time() - decision_time
                else:
                    print('Getting decision from human')
                    decision = self.wait_for_decision(self._current_hand_users[i])
                    self._current_hand_users[i].signal_processed_decision()
                if decision is None:
                    print('No decision from user')
                    decision = Decision(Decision.FOLD)
                    self._current_hand_users[i].is_seated = False
                if decision.bet_ammount is not None:
                    if not self._check_bet_ammount(decision.bet_ammount, self._current_hand_users[i]):
                        decision = Decision(Decision.CHECK)
                if decision_time is not None:
                    decision_time = float(str(decision_time))
                    if decision_time < 2:
                        time.sleep(2 - decision_time)
                self._current_hand_users[i].is_active = False
                self._alter_on_decision(self._current_hand_users[i], decision)
            for user in self._to_remove:
                self._table.remove_current_hand_user(user)
            self._current_hand_users = list(filter(lambda u: u.id not in [u2.id for u2 in self._to_remove], self._current_hand_users))
            continue_betting = False
            max_bet = self._get_max_bet()
            for user in self._current_hand_users:
                if user.current_bet < max_bet and user.balance != 0:
                    print(f'Continuing betting because user.current_bet={user.current_bet} and max_bet={max_bet}')
                    continue_betting = True
                    break
        self._update_to_redis()

    def _get_max_bet(self):
        max_bet = 0
        for user in self._current_hand_users:
            max_bet = max(max_bet, user.current_bet)
        return max_bet

    def _can_take_action(self, user):
        if user.balance == 0:
            return False
        max_bet = self._get_max_bet()
        if max_bet == 0:
            return True
        if user.current_bet == max_bet:
            if user.current_bet == self._table.bb and len(self._table.cards) == 0 and user.position == Position.BB:
                return True
            return False
        return True

    def _check_bet_ammount(self, bet_ammount, user):
        if bet_ammount == user.balance:
            return True
        if bet_ammount > user.balance:
            return False 
        if bet_ammount < self._table.bb or bet_ammount < 2 * self._table.current_bet:
            return False
        return True

    def _distribute_cards(self):
        for i, user in enumerate(self._current_hand_users):
            card_0 = generate_random(self._table.used_cards)
            self._table.append_used_card(card_0)
            card_1 = generate_random(self._table.used_cards)
            self._table.append_used_card(card_1)
            self._current_hand_users[i].hand = [card_0, card_1]

    def _decide_winner(self):
        print(f'Deciding winner len is: {len(self._current_hand_users)}')
        board = [c.to_pokereval() for c in self._table.cards]
        winner = None
        max_score = -1
        for i, user in enumerate(self._current_hand_users):
            hole = [c.to_pokereval() for c in user.hand]
            score = HandEvaluator.evaluate_hand(hole, board)
            if score > max_score:
                winner = self._current_hand_users[i]
                max_score = score
        print(f'Pot is: {self._table.pot}')
        winner.balance += self._table.pot

    def _sort_current_hand_users_by_pos(self, start_pos):
        print(f'Sorting by: {start_pos}')
        if start_pos == Position.D:
            self._current_hand_users = sorted(self._current_hand_users, key=lambda u: u.position.index)
            print([u.position.position for u in self._current_hand_users])
            return
        self._sort_current_hand_users_by_pos(Position.D)
        new_current_hand_users = []
        position_index = len(self._current_hand_users)
        for i in range(len(self._current_hand_users)):
            if self._current_hand_users[i].position.index >= start_pos.index:
                position_index = i
                break
        for i in range(position_index, len(self._current_hand_users)):
            new_current_hand_users.append(self._current_hand_users[i])
        for i in range(0, position_index):
            new_current_hand_users.append(self._current_hand_users[i])
        self._current_hand_users = new_current_hand_users
        print([u.position.position for u in self._current_hand_users])

    def _clear(self):
        for i, _ in enumerate(self._current_users):
            self._current_users[i].clear()
        self._table.clear()

    def _update_to_redis(self):
        for user in self._current_users:
            user.update_to_redis()
        self._table.current_users_ids = Table.from_redis(self._table.id).current_users_ids
        self._table.update_to_redis()

    def _alter_on_decision(self, user, decision):
        print(self._table.current_bet, user.current_bet)
        if decision == Decision.FOLD or (decision == Decision.CHECK and self._table.current_bet > user.current_bet and user.balance != 0):
            user.hand = []
            self._to_remove.append(user)
        elif decision == Decision.CHECK:
            return
        elif decision == Decision.CALL:
            decision.bet_ammount = self._table.current_bet - user.current_bet
            bet = user.bet(decision.bet_ammount)
            self._table.bet(bet, user.current_bet)
        else:
            bet = user.bet(decision.bet_ammount)
            self._table.bet(bet, user.current_bet)
            
    def wait_for_decision(self, user):
        if user.balance == 0:
            return Decision(Decision.CHECK)
        poll_tries = 100
        interval = Decision.DECISION_TIME / (poll_tries - 1) 
        for _ in range(poll_tries):
            user = User.from_redis(user.id)
            if user.decision is not None:
                print(f'got decision from user: {user.decision.decision}')
                decision = user.decision
                user.decision = None
                return decision
            time.sleep(interval)
        return None

    def to_json_for_user(self, user_id):
        json_ = {}
        json_['board'] = {}
        json_['board']['cards'] = [str(card) for card in self._table.cards]
        json_['board']['pot'] = self._table.pot
        json_['board']['bb'] = self._table.bb
        json_['users'] = []

        def add_user(user):
            cards = []
            if self._cards_visible or user.id == user_id:
                cards = user.hand
            elif len(user.hand) != 0:
                cards = ['back', 'back']
            json_['users'].append({'active': user.is_active,
                'seated': True,
                'balance': user.balance,
                'dealer': True if user.position == 'D' else False,
                'name': Cred.from_redis(user.id).username,
                'bet': user.current_bet,
                'cards': [str(card) for card in cards],
                'pl': user.pl})

        def add_blank_user():
            json_['users'].append({'active': False,
                'seated': False,
                'balance': 0,
                'dealer': False,
                'name': '',
                'bet': 0,
                'cards': [],
                'pl': 0})

        index = None
        for i, user in enumerate(self._current_users):
            if user.id == user_id:
                index = i
                break
        # TODO: handle heads up case
        if len(self._current_users) <= 2:
            pass
        else:
            add_user(self._current_users[index - 2])
            add_user(self._current_users[index - 1])
            for user in self._current_users[index:]:
                if user.id == self._current_users[index - 2].id or user.id == self._current_users[index - 1]:
                    break
                add_user(user)
            for user in self._current_users[:index - 2]:
                if user.id == self._current_users[index - 2].id or user.id == self._current_users[index - 1]:
                    break
                add_user(user)
        while len(json_['users']) < 6:
            add_blank_user()
        json_['your_index'] = 2
        return json.dumps(json_)

    def update_to_redis_periodically(self):
        while True:
            for user in self._current_users:
                g_redis.set_raw(f'game#{self._table.id}#{user.id}', self.to_json_for_user(user.id))
            time.sleep(0.1)
