# -*- coding: utf-8 -*-
"""*slice_widgets.py* file.

This file contains graphical elements to process slices on images in a widget.

.. note:: LEnsE - Institut d'Optique - version 1.0

.. moduleauthor:: Julien VILLEMEJANE (PRAG LEnsE) <julien.villemejane@institutoptique.fr>
Creation : sep/2025
"""
from lensepy import *
from lensepy.css import *
import sys, os
import numpy as np
from lensepy.pyqt6.widget_combobox import *
from lensepy.pyqt6.widget_slider import *
from lensepy.pyqt6.widget_image_display import *
from lensepy.pyqt6.widget_xy_chart import *
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QLineEdit, QProgressBar,
    QMessageBox, QFileDialog, QMainWindow
)
from PyQt6.QtCore import pyqtSignal, QDir
from matplotlib import pyplot as plt


# TO MOVE TO LENSEPY.PYQT6
from lensepy.images.processing import *
from enum import Enum



class SlicesOptionsWidget(QWidget):
    """
    Widget containing the smooth filters options.
    """

    options_changed = pyqtSignal(str)

    def __init__(self, parent):
        """
        Default Constructor.
        :param parent: Parent window of the main widget.
        """
        super().__init__(parent=None)
        self.layout = QVBoxLayout()
        self.parent = parent

        self.slider_horizontal = SliderBloc(name=translate('vertical_slice'), unit='',
                                      min_value=0, max_value=5, integer=True)
        self.slider_horizontal.set_value(1)
        self.slider_horizontal.slider_changed.connect(self.action_slider_changed)

        self.slider_vertical = SliderBloc(name=translate('horizontal_slice'), unit='',
                                      min_value=0, max_value=5, integer=True)
        self.slider_vertical.set_value(1)
        self.slider_vertical.slider_changed.connect(self.action_slider_changed)

        self.layout.addWidget(self.slider_horizontal)
        self.layout.addWidget(self.slider_vertical)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_sliders_range(self, height, width):
        """Update Sliders range. """
        self.slider_vertical.set_min_max_slider_values(1, height)
        self.slider_horizontal.set_min_max_slider_values(1, width)

    def action_slider_changed(self, event):
        """Action performed when a button is clicked."""
        sender = self.sender()
        self.options_changed.emit('tools_slice')

    def get_slices_values(self):
        """Returns pixels values for horizontal and vertical slices in the image."""
        vert = int(self.slider_vertical.get_value())
        hor = int(self.slider_horizontal.get_value())
        return hor, vert

    def get_selection(self, image: np.ndarray):
        k_size = self.kernel_choice.get_kernel_size()
        if self.filter == Smooth.BLUR:
            output_image = cv2.blur(image, (k_size, k_size))
        elif self.filter == Smooth.GAUSS:
            sigma_x = self.slider_sigma.get_value()
            output_image = cv2.GaussianBlur(image, (k_size, k_size), sigmaX=sigma_x)
        elif self.filter == Smooth.MEDIAN:
            output_image = cv2.medianBlur(image, k_size)
        else:
            return None
        return output_image


class SliceView(XYChartWidget):
    """
    Widget containing a XY chart.
    """

    def __init__(self, parent):
        """
        Default Constructor.
        :param parent: Parent window of the main widget.
        """
        super().__init__(parent=parent)
        self.__show_grid = True

    def show_grid(self, value=True):
        """Change the grid display."""
        self.__show_grid = value

    def refresh_chart(self, last: int = 0):
        super().refresh_chart(last)
        self.plot_chart_widget.showGrid(x=self.__show_grid, y=self.__show_grid)


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle(translate("window_title_main_menu_widget"))
            self.setGeometry(100, 200, 800, 600)

            self.central_widget = SlicesOptionsWidget(self)
            self.central_widget.set_sliders_range(10, 20)
            self.setCentralWidget(self.central_widget)


    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())