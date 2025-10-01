from lensepy import translate
from lensepy.css import *
from PyQt6.QtWidgets import (
    QMainWindow, QSizePolicy,
    QHBoxLayout, QVBoxLayout,
    QLabel, QWidget, QPushButton
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _app.main_manager import MainManager

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self, parent):
        super().__init__()
        self.parent: MainManager = parent
        self.menu_container = QWidget()
        self.menu_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_button_list = []

        ## MAKE A DIFFERENT WIDGET FOR TITLE AND LOGO !!!

        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)

        title2 = QLabel('Right')
        title2.setStyleSheet(styleH1)
        self.right_layout.addWidget(title2)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.menu_container, 1)  # 1/7
        main_layout.addWidget(self.right_container, 6)  # 6/7

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_menu_elements(self, elements: list):
        """

        :param elements: List of graphical elements to add.
        """
        self._clear_menu_layout()
        # Logo
        if self.parent.app_logo != '':
            app_logo = QLabel('Logo')
            app_logo.setScaledContents(True)
            app_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo = QPixmap(self.parent.app_logo)
            app_logo = LogoLabel(logo)
            self.menu_layout.addWidget(app_logo)
        # Title

        self.menu_layout.addStretch()
        for element in elements:
            b_title = translate(f'{element}_menu')
            button = QPushButton(b_title)
            button.clicked.connect(self.handle_main_menu)
            button.setStyleSheet(unactived_button)
            button.setFixedHeight(BUTTON_HEIGHT)
            self.menu_button_list.append(button)
            self.menu_layout.addWidget(button)

    def handle_main_menu(self, event):
        print(event)

    def _clear_menu_layout(self):
        while self.menu_layout.count():
            item = self.menu_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Destroy widget

    def set_right_widget(self, widget: QWidget):
        """
        Set the right widget of the main window.
        :param widget:  Widget to input in the right section of the window.
        """
        self.right_layout.addWidget(widget)

    def set_mode1(self):
        """Disposition 2x2 (par défaut)"""
        pass

    def set_mode2(self):
        """Disposition 1/4 - 3/4 sur hauteur et 2/7 - 4/7 sur largeur"""
        pass

    def closeEvent(self, event):
        print('End of application')


class LogoLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        print(f'W = {self.width()} / H = {self.height()}')
        scaled_pixmap = self.original_pixmap.scaled(
            self.width(),
            self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        super().resizeEvent(event)