from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage

class Form:
    def __init__(self, label_text, is_password=False):
        self.layout = QVBoxLayout()
        self.error_label = QLabel()
        self.error_label.setStyleSheet('QLabel {color : red; }')
        self.label = QLabel()
        self.label.setText(label_text)
        self.line_edit = QLineEdit()
        if is_password:
            self.line_edit.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

    def add_to_layout(self, layout):
        layout.addLayout(self.layout)

    def get_text(self):
        return self.line_edit.text()

    def set_error_text(self, error_text):
        self.error_label.setText(error_text)
