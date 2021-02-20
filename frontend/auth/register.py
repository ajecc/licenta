from form import Form
from request import g_request
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login_window = None
        self.init_window()
        self.init_layouts()
        self.add_forms()
        self.add_buttons()

    def init_window(self):
        self.register_window = None
        self.setWindowTitle('Register')
    
    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.forms_layout = QVBoxLayout(self)
        self.buttons_layout = QHBoxLayout(self)
        # Adding to the main_layout
        self.main_layout.addLayout(self.forms_layout)
        self.main_layout.addLayout(self.buttons_layout)

    def add_forms(self):
        # Email 
        self.email_form = Form('Email')
        self.email_form.add_to_layout(self.forms_layout)
        # Username
        self.username_form = Form('Username')
        self.username_form.add_to_layout(self.forms_layout)
        # Password
        self.password_form = Form('Password', is_password=True)
        self.password_form.add_to_layout(self.forms_layout)

    def add_buttons(self):
        # Register
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register_button_action)
        self.buttons_layout.addWidget(self.register_button)
        # Login
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login_button_action)
        self.buttons_layout.addWidget(self.login_button)

    def login_button_action(self):
        self.login_window.show()
        self.hide()
        
    def register_button_action(self):
        self.email_form.set_error_text('')
        self.username_form.set_error_text('')
        self.password_form.set_error_text('')
        email = self.email_form.get_text()
        username = self.username_form.get_text()
        password = self.password_form.get_text()
        status, data = g_request.register(email, username, password)
        if status != 200:
            if 'email' in data.lower():
                self.email_form.set_error_text(data)
            if 'username' in data.lower():
                self.username_form.set_error_text(data)
            if 'password' in data.lower():
                self.password_form.set_error_text(data)
        print(status, data)
