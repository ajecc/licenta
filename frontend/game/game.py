from common.form import Form
from common.request import g_request
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage, QGridLayout, QMainWindow
from PyQt5 import QtGui, QtCore
import json
from game.user import UserWidget
from game.image import ImageWidget
from common.request import g_request
import time


LOOP_TIME = 100  # ms


class GameLayout(QVBoxLayout):
    def __init__(self, game_state_json):
        super().__init__()
        self._game_state = json.loads(game_state_json)
        self._your_user = self._game_state['users'][self._game_state['your_index']]
        self._init_layouts()
        self._add_cards_to_board(self._game_state['board']['cards'])
        for user in self._game_state['users']:
            if user['seated']:
                self._add_user(user)
        if self._your_user['active']:
            self._add_buttons()

    def _init_layouts(self):
        self._board_layout = QHBoxLayout()
        self._board_layout.setAlignment(QtCore.Qt.AlignCenter)
        self._users_layout = QHBoxLayout()
        self._users_layout.setAlignment(QtCore.Qt.AlignCenter)
        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.setAlignment(QtCore.Qt.AlignCenter)
        self._buttons_layout.setContentsMargins(420, 30, 420, 100)
        self.addLayout(self._board_layout)
        self.addLayout(self._users_layout)
        self.addLayout(self._buttons_layout)

    def _add_user(self, user_json):
        self._users_layout.addWidget(UserWidget(user_json))

    def _add_cards_to_board(self, cards):
        for card in cards:
            card = ImageWidget(card)
            self._board_layout.addWidget(card)

    def _add_buttons(self):
        self._bet_line_edit = QLineEdit()
        self._validator = QtGui.QIntValidator(self._find_min_bet(), self._your_user['balance'])
        self._bet_line_edit.setValidator(self._validator)
        self._bet_line_edit.setAlignment(QtCore.Qt.AlignRight)
        self._bet_button = QPushButton('Bet')
        self._bet_button.clicked.connect(self._send_bet_decision)
        self._call_button = QPushButton('Call')
        self._call_button.clicked.connect(self._send_call_decision)
        self._check_button = QPushButton('Check')
        self._check_button.clicked.connect(self._send_check_decision)
        self._fold_button = QPushButton('Fold')
        self._fold_button.clicked.connect(self._send_check_decision)
        if not self._your_user['active']:
            return
        self._buttons_layout.addWidget(self._bet_line_edit)
        self._buttons_layout.addWidget(self._bet_button)
        if self._your_user['bet'] >= max([user['bet'] for user in self._game_state['users']]):
            self._buttons_layout.addWidget(self._check_button)
        else:
            self._buttons_layout.addWidget(self._call_button)
            self._buttons_layout.addWidget(self._fold_button)

    def _send_check_decision(self):
        g_request.post_decision({'decision': 'CHECK'})

    def _send_call_decision(self):
        g_request.post_decision({'decision': 'CALL'})

    def _send_bet_decision(self):
        bet_text = self._bet_line_edit.text()
        if len(bet_text) == 0:
            bet_text = 0
        bet_ammount = int(bet_text) 
        if bet_ammount < self._find_min_bet():
            print(f'ERROR: invalid bet ammount: {bet_ammount}')
        else:
            g_request.post_decision({'decision': 'BET', 'bet_ammount': bet_ammount})
    
    def _find_min_bet(self):
        max_bet = 0
        second_max_bet = 0
        for user in self._game_state['users']:
            if user['bet'] > max_bet:
                max_bet = user['bet']
                second_max_bet = max_bet
            elif user['bet'] >= self._game_state['board']['bb'] and user['bet'] > second_max_bet:
                second_max_bet = user['bet']
        bet_ammount = max_bet - second_max_bet
        bet_ammount = max(bet_ammount, self._game_state['board']['bb'])
        if bet_ammount > self._your_user['balance']:
            bet_ammount = self._your_user['balance']
        return bet_ammount


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_window()
        self._main_layout = QVBoxLayout(self) 
        self._game_layout = None
        self._last_game_text = ''

    def _init_window(self):
        self.setWindowTitle('Game')
        self.setFixedHeight(600)
        self.setFixedWidth(1200)

    def set_layout(self, layout):
        if self._game_layout is not None:
            self._game_layout.setParent(None)
            del self._game_layout
        self._game_layout = layout
        # self._game_layout.setParent(self)
        self._main_layout.addLayout(self._game_layout)
        self.widget = QWidget()
        self.widget.setLayout(self._main_layout)
        self.setCentralWidget(self.widget)

    def run_game_loop(self):
        self._timer = QtCore.QTimer() 
        self._timer.timeout.connect(self._update)
        self._timer.start(LOOP_TIME)

    def _update(self):
        # status, game_text = 200, open('assets/example.json').read()
        status, game_text = g_request.get_game_state()
        if status != 200:
            print(f'Error interacting from server: {game_text}')
        if len(game_text) < 2:
            print("Didn't receive valid game text yet")
            return
        print(game_text)
        if self._last_game_text == game_text:
            game_state = json.loads(game_text)
            your_user = game_state['users'][game_state['your_index']]
            if your_user['active']:
                return
        self._last_game_text = game_text
        game_layout = GameLayout(game_text)
        self.set_layout(game_layout)
