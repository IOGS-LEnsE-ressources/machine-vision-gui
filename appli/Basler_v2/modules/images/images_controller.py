from PyQt6.QtWidgets import QWidget
from _app.template_controller import TemplateController
from modules.images.images_views import *

class ImagesController(TemplateController):
    """

    """

    def __init__(self, parent=None):
        """

        """
        super().__init__(parent)
        self.top_left = ImagesTopLeftWidget(self)
        self.bot_left = ImagesBotLeftWidget()
        self.bot_right = ImagesOpeningWidget(self)

    def handle_controller(self, event):
        super().handle_controller(event)
        print("Event New")


        