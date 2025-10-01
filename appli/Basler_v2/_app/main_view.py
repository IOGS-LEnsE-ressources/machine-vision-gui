from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget

from _app.lense_view import LEnsEView

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.menu_layout = QVBoxLayout()
        title1 = QLabel('Test')
        self.menu_layout.addWidget(title1)

        self.right_layout = QVBoxLayout()
        title2 = QLabel('Right')
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

    def mode1(self):
        """Disposition 2x2 (par défaut)"""
        self.clear_central()

        top_split = QSplitter(Qt.Orientation.Horizontal)
        bot_split = QSplitter(Qt.Orientation.Horizontal)

        # Top
        top_left = QLabel("Top Left")
        top_left.setStyleSheet("background-color: lightblue;")
        top_right = QLabel("Top Right")
        top_right.setStyleSheet("background-color: lightgreen;")
        top_split.addWidget(top_left)
        top_split.addWidget(top_right)
        top_split.setSizes([1, 1])  # moitié-moitié

        # Bottom
        bot_left = QLabel("Bot Left")
        bot_left.setStyleSheet("background-color: orange;")
        bot_right = QLabel("Bot Right")
        bot_right.setStyleSheet("background-color: pink;")
        bot_split.addWidget(bot_left)
        bot_split.addWidget(bot_right)
        bot_split.setSizes([1, 1])

        # Split vertical (haut/bas)
        vert_split = QSplitter(Qt.Orientation.Vertical)
        vert_split.addWidget(top_split)
        vert_split.addWidget(bot_split)
        vert_split.setSizes([1, 1])  # moitié-moitié

        self.central_layout.addWidget(vert_split)

    def mode2(self):
        """Disposition 1/4 - 3/4 sur hauteur et 2/7 - 4/7 sur largeur"""
        self.clear_central()

        # Split vertical 1/4 - 3/4
        vert_split = QSplitter(Qt.Orientation.Vertical)

        top = QLabel("Top (1/4 hauteur)")
        top.setStyleSheet("background-color: lightyellow;")
        bottom = QLabel("Bottom (3/4 hauteur)")
        bottom.setStyleSheet("background-color: lightcoral;")

        vert_split.addWidget(top)
        vert_split.addWidget(bottom)
        vert_split.setSizes([1, 3])  # ratio 1/4 - 3/4

        # Split horizontal 2/7 - 4/7
        hor_split = QSplitter(Qt.Orientation.Horizontal)
        left = QLabel("Left (2/7 largeur)")
        left.setStyleSheet("background-color: lightcyan;")
        right = vert_split  # stack vertical à droite

        hor_split.addWidget(left)
        hor_split.addWidget(right)
        hor_split.setSizes([2, 4])  # ratio 2/7 - 4/7

        self.central_layout.addWidget(hor_split)
