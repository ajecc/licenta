import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow
from register import RegisterWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)     
    login_window = LoginWindow()
    register_window = RegisterWindow()
    login_window.register_window = register_window
    register_window.login_window = login_window
    login_window.show()
    sys.exit(app.exec_())
