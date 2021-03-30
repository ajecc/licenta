import sys
from PyQt5.QtWidgets import QApplication
from auth.login import LoginWindow
from auth.register import RegisterWindow
from settings.settings import SettingsWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)     
    login_window = LoginWindow()
    register_window = RegisterWindow()
    settings_window = SettingsWindow()
    login_window.register_window = register_window
    register_window.login_window = login_window
    login_window.settings_window = settings_window
    register_window.settings_window = settings_window
    login_window.show()
    sys.exit(app.exec_())
