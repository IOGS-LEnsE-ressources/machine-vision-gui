from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DefaultTopLeftWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(0, 100, 0);")
        layout = QVBoxLayout()
        label = QLabel('Top Left')
        layout.addWidget(label)
        self.setLayout(layout)

class DefaultBotLeftWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(0, 0, 100);")
        layout = QVBoxLayout()
        label = QLabel('Bot Left')
        layout.addWidget(label)
        self.setLayout(layout)