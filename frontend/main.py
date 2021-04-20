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
    login_window = LoginWindow()
    register_window = RegisterWindow()
    game_window = GameWindow()
    settings_window = SettingsWindow()
    login_window.register_window = register_window
    register_window.login_window = login_window
    login_window.settings_window = settings_window
    register_window.settings_window = settings_window
    settings_window.game_window = game_window
    login_window.show()
    sys.exit(app.exec_())
