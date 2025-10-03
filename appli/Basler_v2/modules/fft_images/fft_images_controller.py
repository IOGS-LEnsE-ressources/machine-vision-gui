from PyQt6.QtWidgets import QWidget
import numpy as np
from _app.template_controller import TemplateController
from modules.fft_images.fft_images_views import *
from lensepy.pyqt6.widget_image_display import ImageDisplayWidget


class FFTImagesController(TemplateController):
    """

    """

    def __init__(self, parent=None):
        """

        """
        super().__init__(parent)
        self.top_left = ImageDisplayWidget()
        self.bot_left = HistogramWidget()
        self.bot_right = ImagesOpeningWidget(self)
        self.top_right = ImagesInfosWidget(self)
        # Setup widgets
        self.bot_left.set_background('white')
        self.bot_left.set_bits_depth(8)
        self.bot_left.refresh_chart()
        # Signals
        self.bot_right.image_opened.connect(self.action_image_opened)

    def action_image_opened(self, event):
        """
        Action performed when an image is opened via the bot_right widget.
        :return:
        """
        image = self.get_variables()['image']
        # Display image
        self.display_image(image)
        # Update histogram
        self.bot_left.set_image(image)
        self.bot_left.refresh_chart()
        # Update image information
        self.top_right.update_infos(image)

    def display_image(self, image: np.ndarray):
        """
        Display the image given as a numpy array.
        :param image:   numpy array containing the data.
        :return:
        """
        self.top_left.set_image_from_array(image)


