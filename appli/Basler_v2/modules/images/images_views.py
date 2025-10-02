from lensepy import translate
from lensepy.css import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame
from lensepy.pyqt6.widget_image_display import ImageDisplayWidget

class ImagesTopLeftWidget(ImageDisplayWidget):
    """

    """
    def __init__(self, parent=None):
        super().__init__(parent)

class ImagesBotLeftWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(100, 0, 100);")
        layout = QVBoxLayout()
        label = QLabel('IMAGE Bot Left')
        layout.addWidget(label)
        self.setLayout(layout)

class ImagesOpeningWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(None)
        self.parent = parent
        layout = QVBoxLayout()

        h_line = QFrame()
        h_line.setFrameShape(QFrame.Shape.HLine)  # Trait horizontal
        h_line.setFrameShadow(QFrame.Shadow.Sunken)  # Effet "enfoncé" (optionnel)
        layout.addWidget(h_line)

        label = QLabel(translate('image_opening_dialog'))
        label.setStyleSheet(styleH2)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        open_button = QPushButton(translate('image_opening_button'))
        open_button.setStyleSheet(unactived_button)
        open_button.setFixedHeight(BUTTON_HEIGHT)
        open_button.clicked.connect(self.handle_opening)
        layout.addWidget(open_button)

        layout.addStretch()
        self.setLayout(layout)

    def handle_opening(self):
        sender = self.sender()
