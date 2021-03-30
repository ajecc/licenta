from common.form import Form
from common.request import g_request
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._register_window = None
        self._settings_window = None
        self._init_window()
        self._init_layouts()
        self._add_forms()
        self._add_buttons()

    def _init_window(self):
        self.setWindowTitle('Login')
    
    def _init_layouts(self):
        self._main_layout = QVBoxLayout(self)
        self._forms_layout = QVBoxLayout(self)
        self._buttons_layout = QHBoxLayout(self)
        # Adding to the main_layout
        self._main_layout.addLayout(self._forms_layout)
        self._main_layout.addLayout(self._buttons_layout)

    def _add_forms(self):
        # Username
        self._username_form = Form('Username')
        self._username_form.add_to_layout(self._forms_layout)
        # Password
        self._password_form = Form('Password', is_password=True)
        self._password_form.add_to_layout(self._forms_layout)

    def _add_buttons(self):
        # Login
        self._login_button = QPushButton('Login')
        self._login_button.clicked.connect(self._login_button_action)
        self._buttons_layout.addWidget(self._login_button)
        # Register
        self._register_button = QPushButton('Register')
        self._register_button.clicked.connect(self._register_button_action)
        self._buttons_layout.addWidget(self._register_button)

    def _login_button_action(self):
        self._username_form.set_error_text('')
        self._password_form.set_error_text('')
        username = self._username_form.get_text()
        password = self._password_form.get_text()
        status, data = g_request.login(username, password)
        if status != 200:
            self._username_form.set_error_text(data)
        else:
            self._settings_window.show()
            self.hide()
        print(status, data)
        
    def _register_button_action(self):
        self._register_window.show()
        self.hide()

    @property
    def register_window(self):
        return self._register_window
    
    @register_window.setter
    def register_window(self, value):
        self._register_window = value

    @property
    def settings_window(self):
        return self._settings_window
    
    @settings_window.setter
    def settings_window(self, value):
        self._settings_window = value
