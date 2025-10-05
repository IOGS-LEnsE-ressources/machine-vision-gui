from PyQt6.QtWidgets import QWidget
import numpy as np
from _app.template_controller import TemplateController
from lensepy.pyqt6.widget_image_display import ImageDisplayWidget


class TestController(TemplateController):
    """

    """

    def __init__(self, parent=None):
        """

        """
        super().__init__(parent)
        self.top_left = QWidget()
        self.bot_left = QWidget()
        self.bot_right = QWidget()
        self.top_right = QWidget()