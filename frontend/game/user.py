from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from game.image import ImageWidget
import json

class UserWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self._user = user
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignCenter)
        self._layout.addStretch()
        self._bet_layout = QHBoxLayout()
        self._layout.addLayout(self._bet_layout)
        self._add_bet_elems()
        self._add_cards()
        self._add_info()
        self._layout.addStretch()
        self._layout.setSpacing(1)

    def _add_cards(self):
        self._cards_layout = QHBoxLayout()
        self._cards_layout.addStretch()
        if len(self._user['cards']) == 0:
            self._user['cards'] = ['blank', 'blank']
        elif len(self._user['cards']) == 1:
            self._user['cards'].append('back')
        self._card_0 = ImageWidget(self._user['cards'][0])
        self._card_1 = ImageWidget(self._user['cards'][1])
        self._cards_layout.addWidget(self._card_0)
        self._cards_layout.addWidget(self._card_1)
        self._cards_layout.addStretch()
        self._cards_layout.setSpacing(2)
        self._layout.addLayout(self._cards_layout)

    def _add_info(self):
        self._info_layout = QVBoxLayout()
        self._name_label = QLabel('name:     ' + str(self._user['name']))
        self._balance_label = QLabel('balance: ' + str(self._user['balance']))
        self._name_label.setAlignment(Qt.AlignCenter)
        self._balance_label.setAlignment(Qt.AlignCenter)
        self._info_layout.addWidget(self._name_label)
        self._info_layout.addWidget(self._balance_label)
        if self._user['active']:
            self._info_layout.addWidget(ImageWidget('active', scale=(20, 20)))
        self._layout.addLayout(self._info_layout)

    def _add_bet_elems(self):
        if self._user['bet'] != 0:
            bet_label = QLabel('Bet:  ' + str(self._user['bet']))
            self._bet_layout.addWidget(bet_label)
        if self._user['dealer']:
            image = ImageWidget('dealer', scale=(20, 20))
            image.setAlignment(Qt.AlignRight)
            self._bet_layout.addWidget(image)
        else:
            image = ImageWidget('blank_dealer', scale=(20, 20))
            image.setAlignment(Qt.AlignRight)
            self._bet_layout.addWidget(image)

