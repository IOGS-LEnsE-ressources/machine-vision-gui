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


        self.check_diff = QCheckBox(text=translate('check_diff_image'))
        self.check_diff.stateChanged.connect(self.action_button_clicked)

        self.filter_type = ButtonSelectionWidget(parent=self, name=translate('filtre_type'))
        self.list_options = [translate('filter_blur'),
                             translate('filter_gaussian'),
                             translate('filter_median')]
        self.selected_type = 1
        self.filter_type.set_list_options(self.list_options)
        self.filter_type.clicked.connect(self.action_button_clicked)
        self.filter_type.activate_index(self.selected_type)

        self.kernel_choice = QWidget()

        self.slider_sigma = SliderBloc(name=translate('gaussian_sigma'), unit='',
                                      min_value=0, max_value=5)
        self.slider_sigma.set_value(1)
        self.slider_sigma.set_enabled(False)
        self.slider_sigma.slider_changed.connect(self.action_button_clicked)

        self.layout.addWidget(self.check_diff)
        self.layout.addWidget(self.filter_type)
        self.layout.addWidget(self.kernel_choice)
        self.layout.addStretch()
        self.layout.addWidget(self.slider_sigma)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def action_button_clicked(self, event):
        """Action performed when a button is clicked."""
        sender = self.sender()
        if sender == self.check_diff:
            check_ok = 1 if self.check_diff.isChecked() else 0
            self.options_changed.emit(f'check_diff:{check_ok}')
        elif sender == self.filter_type:
            f_type = self.filter_type.get_selection()
            self.slider_sigma.set_enabled(False)
            if f_type == translate('filter_blur'):
                self.filter = Smooth.BLUR
            elif f_type == translate('filter_gaussian'):
                self.filter = Smooth.GAUSS
                self.slider_sigma.set_enabled(True)
            elif f_type == translate('filter_median'):
                self.filter = Smooth.MEDIAN
        elif sender == self.slider_sigma:
            sigma = self.slider_sigma.get_value()

        self.options_changed.emit('smooth_filter')

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


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle(translate("window_title_main_menu_widget"))
            self.setGeometry(100, 200, 800, 600)

            self.central_widget = SlicesOptionsWidget(self)
            self.setCentralWidget(self.central_widget)


    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())