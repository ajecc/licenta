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
            print('sleeping a bit')
            time.sleep(5)
            self._cards_visible = False
            print('updating users')
            self._update_current_users()
            #print('shifting positions')
            #self._shift_users_position()
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
            self._current_users[i].position = Position(index=i)
            self._current_users[i].update_to_redis()

    def _seat_users(self):
        self._current_users = [User.from_redis(id) for id in self._table.current_users_ids]
        for i, _ in enumerate(self._current_users):
            self._current_users[i].is_seated = True
            self._current_users[i].update_to_redis()

    def _update_current_users(self):
        self._table.current_hand_users_ids = []
        new_current_users_ids = []
        for id in self._table._current_users_ids:
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
        self._table.bet(bet)
        bet = self._find_by_position(Position(*Position.BB)).bet(self._table.bb)
        self._table.bet(bet)
        # TODO: handle special case: heads-up
        self._sort_current_hand_users_by_pos(Position(*Position.UTG))
        self._start_betting_round()

    def _find_by_position(self, position):
        for user in self._current_hand_users:
            print(f'user.position = {user.position}')
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
            self._start_betting_round()

    def _shift_users_position(self):
        # TODO: correct this. It is wrong. Find the dealer. 
        # If there is no dealer assign it to the SB and so on 
        # Shift the dealer
        # Then set all positions according to that 
        # TODO: handle heads-up
        new_current_users = []
        for user in self._current_users:
            user.position = user.position.get_next()
            new_current_users.append(user)
        self._current_users = new_current_users

    def _start_betting_round(self):
        # TODO: repeat this
        self._to_remove = []
        for i, _ in enumerate(self._current_hand_users):
            if len(self._to_remove) == len(self._current_hand_users) - 1:
                break
            self._current_hand_users[i].is_active = True
            if self._current_hand_users[i].is_bot:
                # decision = self._ai_bridge.get_decision(self.to_json_for_self._current_hand_users[i](self._current_hand_users[i].id))
                decision = Decision(Decision.FOLD)
            else:
                decision = self.wait_for_decision(self._current_hand_users[i])
                self._current_hand_users[i].signal_processed_decision()
            if decision is None:
                decision = Decision.FOLD
                self._current_hand_users[i].is_seated = False
            if decision.bet_ammount is not None:
                if not self._check_bet_ammount(decision.bet_ammount, self._current_hand_users[i]):
                    decision = Decision(Decision.CHECK)
            self._current_hand_users[i].is_active = False
            self._alter_on_decision(self._current_hand_users[i], decision)
            time.sleep(2)
        for user in self._to_remove:
            self._table.remove_current_hand_user(user)
            self._current_hand_users = list(filter(lambda u: u.id != user.id, self._current_hand_users))
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
        card = generate_random(self._used_cards)
        self._used_cards.append(card)
        self._cards.append(card)
    
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
        winner.balance += self._table.pot

    def _sort_current_hand_users_by_pos(self, start_pos):
        self._current_hand_users = sorted(self._current_hand_users,
                key=lambda u: u.position.index if u.position.index >= start_pos.index else Position(*Position.UTG_2).index + 1 + u.position.index) 

    def _clear(self):
        for i, _ in enumerate(self._current_users):
            self._current_users[i].clear()
        self._table.clear()

    def _update_to_redis(self):
        for user in self._current_users:
            user.update_to_redis()
        self._table.update_to_redis()
    
    def _alter_on_decision(self, user, decision):
        if decision == Decision.FOLD or (decision == Decision.CHECK and self._table.current_bet > user.current_bet and user.current_bet != user.balance):
            user.hand = []
            self._to_remove.append(user)
        elif decision == Decision.CALL:
            decision.bet_ammount = 1  # TODO
        # TODO: this might be wrong. Tweak later
        else:
            bet = user.bet(decision.bet_ammount)
            self._table.bet(bet)
            
    def wait_for_decision(self, user):
        if user.balance == 0:
            return Decision.CHECK
        poll_tries = 100
        interval = Decision.DECISION_TIME / (poll_tries - 1) 
        for _ in range(poll_tries):
            user = User.from_redis(user.id)
            if user.decision is not None:
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
                'cards': [str(card) for card in cards]})

        def add_blank_user():
            json_['users'].append({'active': False,
                'seated': False,
                'balance': 0,
                'dealer': False,
                'name': '',
                'bet': 0,
                'cards': []})

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
                if user.id == self._current_users[index - 2].id:
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
