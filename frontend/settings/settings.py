from common.form import Form
from common.request import g_request
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._game_window = None
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
        # Bots 
        self._bots_form = Form('Number of Bots')
        self._bots_form.add_to_layout(self._forms_layout)
        # Table code
        # self._table_code = Form('Table Code')
        # self._table_code.add_to_layout(self._forms_layout)

    def _add_buttons(self):
        # Login
        self._create_table_button = QPushButton('Create Table')
        self._create_table_button.clicked.connect(self._create_table_button_action)
        self._buttons_layout.addWidget(self._create_table_button)

    def _create_table_button_action(self):
        self._bots_form.set_error_text('')
        bots_cnt = self._bots_form.get_text()
        try:
            bots_cnt = int(bots_cnt)
            if bots_cnt < 1 or bots_cnt > 5:
                raise ValueError()
        except:
            self._bots_form.set_error_text('Number of Bots must be a number between 1 and 5')
            return
        status, data = g_request.create_table(bots_cnt)
        if status != 200:
            self._bots_form.set_error_text(data)
        else:
            self._start_game()

    def _join_button_action(self):
        self._join_form.set_error_text('')
        status, data = g_request.join_table(self._join_form.get_text())
        if status != 200:
            self._join_form.set_error_text(data)
        else:
            self._start_game()

    def _start_game(self):
        self.hide()
        self._game_window.show()
        self._game_window.run_game_loop()
    
    @property
    def game_window(self):
        return self._game_window
   
    @game_window.setter
    def game_window(self, value):
        self._game_window = value
