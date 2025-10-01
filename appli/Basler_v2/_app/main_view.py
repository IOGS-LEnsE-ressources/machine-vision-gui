from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from lensepy.css import *
from _app.lense_view import LEnsEView

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.menu_layout = QVBoxLayout()
        title1 = QLabel('Test')
        title1.setStyleSheet(styleH1)
        self.menu_layout.addWidget(title1)

        self.right_layout = QVBoxLayout()
        title2 = QLabel('Right')
        title2.setStyleSheet(styleH1)
        self.right_layout.addWidget(title2)

        main_layout = QHBoxLayout()
        main_layout.addLayout(self.menu_layout, 1)  # 1/7
        main_layout.addLayout(self.right_layout, 6)  # 6/7

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
