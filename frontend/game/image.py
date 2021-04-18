from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

# CARDS FROM: https://code.google.com/archive/p/vector-playing-cards
# CARD BACK FROM: https://github.com/richardschneider/cardsJS
# DEALER BUTTON FROM: https://www.pngwing.com/en/search?q=dealer+Button

class ImageWidget(QLabel):
    def __init__(self, name, scale=(128, 128), parent=None):
        super().__init__(parent)
        self._pixmap = QtGui.QPixmap(f'assets/{name}.svg')
        # TODO: don't hardcode these
        self._pixmap = self._pixmap.scaled(scale[0], scale[1], Qt.KeepAspectRatio)
        self.setPixmap(self._pixmap)
        self.setAlignment(Qt.AlignCenter)

