from form import Form
from request import g_request
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.register_window = None
        self.init_window()
        self.init_layouts()
        self.add_forms()
        self.add_buttons()

    def init_window(self):
        self.register_window = None
        self.setWindowTitle('Login')
    
    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.forms_layout = QVBoxLayout(self)
        self.buttons_layout = QHBoxLayout(self)
        # Adding to the main_layout
        self.main_layout.addLayout(self.forms_layout)
        self.main_layout.addLayout(self.buttons_layout)

    def add_forms(self):
        # Username
        self.username_form = Form('Username')
        self.username_form.add_to_layout(self.forms_layout)
        # Password
        self.password_form = Form('Password', is_password=True)
        self.password_form.add_to_layout(self.forms_layout)

    def add_buttons(self):
        # Login
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login_button_action)
        self.buttons_layout.addWidget(self.login_button)
        # Register
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register_button_action)
        self.buttons_layout.addWidget(self.register_button)

    def login_button_action(self):
        self.username_form.set_error_text('')
        self.password_form.set_error_text('')
        username = self.username_form.get_text()
        password = self.password_form.get_text()
        status, data = g_request.login(username, password)
        if status != 200:
            self.username_form.set_error_text(data)
        print(status, data)
        
    def register_button_action(self):
        self.register_window.show()
        self.hide()


