from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from auth.login import LoginWindow
from auth.register import RegisterWindow
from settings.settings import SettingsWindow
from game.game import GameWindow, GameLayout

if __name__ == '__main__':
    app = QApplication(sys.argv)     
    #login_window = LoginWindow()
    #register_window = RegisterWindow()
    #settings_window = SettingsWindow()
    #login_window.register_window = register_window
    #register_window.login_window = login_window
    #login_window.settings_window = settings_window
    #register_window.settings_window = settings_window
    #login_window.show()
    game_window = GameWindow()
    game_window.set_layout(GameLayout(open('assets/example.json').read(), (500, 500)))
    game_window.show()
#    game_window.set_layout(GameLayout('{}', (500, 500)))
    sys.exit(app.exec_())
