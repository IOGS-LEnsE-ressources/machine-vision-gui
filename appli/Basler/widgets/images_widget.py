# -*- coding: utf-8 -*-
"""*images_widget.py* file.

This file contains graphical elements to display images in a widget.
Image is coming from a file (JPG, PNG...) or an industrial camera (IDS, Basler...).

.. note:: LEnsE - Institut d'Optique - version 1.0

.. moduleauthor:: Julien VILLEMEJANE (PRAG LEnsE) <julien.villemejane@institutoptique.fr>
Creation : oct/2024
"""
import sys, os
import numpy as np
import cv2
from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QCheckBox,
    QMessageBox, QFileDialog, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt, pyqtSignal
from lensepy import load_dictionary, translate
from lensepy.css import *
from widgets.camera import *


class ImagesFileOpeningWidget(QWidget):
    """
    Options widget of the image opening menu.
    """

    image_opened = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        """
        Default Constructor.
        :param parent: Parent widget of this widget.
        """
        super().__init__(parent=parent)
        # GUI Structure
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.button_open_image = QPushButton(translate('button_open_image_from_file'))
        self.button_open_image.setStyleSheet(unactived_button)
        self.button_open_image.setFixedHeight(BUTTON_HEIGHT)
        self.button_open_image.clicked.connect(self.action_open_image)

        self.layout.addWidget(self.button_open_image)
        self.layout.addStretch()

    def action_open_image(self, event, gray: bool=True):
        """
        Open an image from a file.
        """
        self.button_open_image.setStyleSheet(actived_button)
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, translate('dialog_open_image'),
                                                   "", "Images (*.png *.jpg *.jpeg)")
        if file_path != '':
            if gray:
                image_array = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            else:
                image_array = cv2.imread(file_path)
            self.image_opened.emit(image_array)
        else:
            self.button_open_image.setStyleSheet(unactived_button)
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning - No File Loaded")
            dlg.setText("No Image File was loaded...")
            dlg.setStandardButtons(
                QMessageBox.StandardButton.Ok
            )
            dlg.setIcon(QMessageBox.Icon.Warning)
            button = dlg.exec()


class ImagesCameraOpeningWidget(QWidget):
    """
    Options widget of the image opening menu.
    """

    camera_opened = pyqtSignal(dict)

    def __init__(self, parent=None):
        """
        Default Constructor.
        :param parent: Parent widget of this widget.
        """
        super().__init__(parent=parent)
        self.parent = parent
        # GUI Structure
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.button_open_camera = QPushButton(translate('button_open_camera_indus'))
        self.button_open_camera.setStyleSheet(unactived_button)
        self.button_open_camera.setFixedHeight(BUTTON_HEIGHT)
        self.button_open_camera.clicked.connect(self.action_open_camera)

        self.button_open_webcam = QPushButton(translate('button_open_webcam'))
        self.button_open_webcam.setStyleSheet(disabled_button)
        self.button_open_webcam.setFixedHeight(BUTTON_HEIGHT)
        self.button_open_webcam.clicked.connect(self.action_open_webcam)
        self.button_open_webcam.setEnabled(False)

        self.button_open_brand_cam = QLabel('')
        default_brand = 'brandname' in self.parent.default_parameters
        if default_brand:
            self.button_open_brand_cam = QPushButton(translate('button_open_brand_cam'))
            self.button_open_brand_cam.setStyleSheet(unactived_button)
            self.button_open_brand_cam.setFixedHeight(BUTTON_HEIGHT)
            self.button_open_camera.setFixedHeight(OPTIONS_BUTTON_HEIGHT)
            self.button_open_brand_cam.clicked.connect(self.action_open_brand_cam)
            self.layout.addWidget(self.button_open_brand_cam)
            self.layout.addStretch()

        self.layout.addWidget(self.button_open_camera)
        self.layout.addWidget(self.button_open_webcam)
        self.layout.addStretch()

    def action_open_camera(self):
        """
        Open an industrial camera.
        """
        self.button_open_camera.setStyleSheet(actived_button)
        self.repaint()
        self.parent.bot_right_widget = CameraChoice()
        self.parent.bot_right_widget.camera_selected.connect(self.action_camera_selected)
        self.parent.set_bot_right_widget(self.parent.bot_right_widget)

    def action_open_brand_cam(self):
        """
        Open an industrial camera.
        """
        if 'brandname' in self.parent.default_parameters:
            camera = cam_from_brands[self.parent.default_parameters['brandname']]()
            if camera.find_first_camera():
                self.parent.parent.camera = camera
                self.parent.parent.camera.init_camera()
                self.parent.parent.camera_thread.set_camera(self.parent.parent.camera)
                # Init default parameters !
                self.parent.menu_action('images')
                self.parent.init_default_camera_params()
                self.parent.bot_right_widget.update_parameters(auto_min_max=True)

                print(f'Expo = {self.parent.parent.camera.get_exposure()}')
                print(f'FPS  = {self.parent.parent.camera.get_frame_rate()}')
                print(f'Colo = {self.parent.parent.camera.get_color_mode()}')
                print(f'ExpoRange = {self.parent.parent.camera.get_exposure_range()}')

                # Start Thread
                self.parent.parent.image_bits_depth = get_bits_per_pixel(
                    self.parent.parent.camera.get_color_mode())
                self.parent.parent.camera_thread.start()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Warning - No Camera")
                dlg.setText("No camera is connected to this computer...")
                dlg.setStandardButtons(
                    QMessageBox.StandardButton.Ok
                )
                dlg.setIcon(QMessageBox.Icon.Warning)
                button = dlg.exec()

    def action_camera_selected(self, event):
        """Action performed when a camera is selected."""
        self.camera_opened.emit(event)

    def action_open_webcam(self, event):
        """
        Open an industrial camera.
        """
        print(event)
        self.camera_opening.emit('webcam_opening')


class ImagesCreateWidget(QWidget):
    """
    Options widget of the image creating menu.
    """

    image_opened = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        """
        Default Constructor.
        :param parent: Parent widget of this widget.
        """
        super().__init__(parent=parent)
        # GUI Structure
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


class ImagesDisplayWidget(QWidget):
    """
    Widget to display an image.
    """

    def __init__(self, parent=None):
        """
        Default Constructor.
        :param parent: Parent widget of this widget.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.width = 0
        self.height = 0
        # GUI Structure
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Objects
        self.image = None
        self.hline_y = None
        self.vline_x = None
        # GUI Elements
        self.image_display = QLabel('Image to display')
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setScaledContents(False)
        self.layout.addWidget(self.image_display)

    def update_size(self, width, height, aoi: bool = False):
        """
        Update the size of this widget.
        """
        self.width = width
        self.height = height
        if self.image is not None:
            image_to_display = self.image
            if self.image.shape[1] > self.width or self.image.shape[0] > self.height:
                image_to_display = resize_image_ratio(self.image, self.height-30, self.width-20)
            qimage = array_to_qimage(image_to_display)
            pmap = QPixmap.fromImage(qimage)
            self.image_display.setPixmap(pmap)

    def set_crosshair(self, x: int = None, y: int = None):
        """
        Place une barre verticale (x) et/ou horizontale (y) sur l'image.
        :param x: Position en pixels de la ligne verticale (None = pas de ligne)
        :param y: Position en pixels de la ligne horizontale (None = pas de ligne)
        """
        self.vline_x = x
        self.hline_y = y
        if self.image is not None:
            self._draw_image_with_lines()

    def set_image_from_array(self, pixels: np.ndarray, aoi: bool = False) -> None:
        """
        Display a new image from an array (Numpy)
        :param pixels: Array of pixels to display.
        :param aoi: If True, print 'AOI' on the image.
        """
        self.image = np.array(pixels, dtype='uint8')
        self._draw_image_with_lines(aoi=aoi)

    def _draw_image_with_lines(self, aoi: bool = False):
        """
        Redessine l'image en ajoutant AOI + lignes si nécessaire.
        """
        image_to_display = self.image
        if self.image.shape[1] > self.width or self.image.shape[0] > self.height:
            if self.width-30 > 0 and self.height-30 > 0:
                image_to_display = resize_image_ratio(self.image, self.height-30, self.width-30)

        qimage = array_to_qimage(image_to_display)
        painter = QPainter(qimage)

        # AOI
        if aoi:
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 15))
            painter.drawText(20, 20, 'AOI')

        # Lignes
        if self.vline_x is not None:
            pen = QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine)  # Rouge
            painter.setPen(pen)
            painter.drawLine(self.vline_x, 0, self.vline_x, qimage.height())

        if self.hline_y is not None:
            pen = QPen(QColor(0, 255, 0), 2, Qt.PenStyle.SolidLine)  # Vert
            painter.setPen(pen)
            painter.drawLine(0, self.hline_y, qimage.width(), self.hline_y)

        painter.end()

        pmap = QPixmap.fromImage(qimage)
        self.image_display.setPixmap(pmap)


# -*- coding: utf-8 -*-
"""*images_display_view.py* file.

./views/images_display_view.py contains ImagesDisplayView and
 ImageToGraphicsScene classes to display images in PyQt6 GUI.

.. note:: LEnsE - Institut d'Optique - version 1.0

.. moduleauthor:: Julien VILLEMEJANE (PRAG LEnsE) <julien.villemejane@institutoptique.fr>
Creation : march/2025
"""
import sys, os
import numpy as np
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QImage, QPainter


class ImagesDisplayView(QGraphicsView):
    """
    Widget to display an image.
    """

    def __init__(self):
        """
        Default Constructor.
        :param parent: Parent widget of this widget.
        """
        super().__init__()
        self.__scene = ImageToGraphicsScene(self)
        self.setScene(self.__scene)

    def set_image(self, image: QImage):
        self.__scene.set_image(image)
        self.update()

    def set_image_from_array(self, np_array: np.array):
        image_disp = np_array.copy().astype(np.uint8)
        height, width, *channels = image_disp.shape
        if channels:
            image = QImage(image_disp, width, height, 3*width, QImage.Format.Format_RGB888)
        else:
            image = QImage(image_disp, width, height, QImage.Format.Format_Grayscale8)
        self.__scene.set_image(image)
        self.update()

class ImageToGraphicsScene(QGraphicsScene):
    def __init__(self, parent: ImagesDisplayView = None):
        super().__init__(parent)
        self.__parent = parent
        self.__image = QImage()

    def set_image(self, image: QImage):
        self.__image = image
        self.update()

    def drawBackground(self, painter: QPainter, rect: QRectF):
        try:
            # Display size
            display_width = self.__parent.width()
            display_height = self.__parent.height()
            # Image size
            image_width = self.__image.width()
            image_height = self.__image.height()

            # Return if we don't have an image yet
            if image_width == 0 or image_height == 0:
                return

            if image_width > display_width or image_height > display_height:
                # Calculate aspect ratio of display
                ratio1 = display_width / display_height
                # Calculate aspect ratio of image
                ratio2 = image_width / image_height

                if ratio1 > ratio2:
                    # The height with must fit to the display height.So h remains and w must be scaled down
                    image_width = display_height * ratio2
                    image_height = display_height
                else:
                    # The image with must fit to the display width. So w remains and h must be scaled down
                    image_width = display_width
                    image_height = display_height / ratio2

            image_pos_x = -1.0 * (image_width / 2.0)
            image_pox_y = -1.0 * (image_height / 2.0)

            # Remove digits after point
            image_pos_x = int(image_pos_x)
            image_pox_y = int(image_pox_y)

            rect = QRectF(image_pos_x, image_pox_y, image_width, image_height)

            painter.drawImage(rect, self.__image)
        except Exception as e:
            print(f'draw_background / {e}')


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import time

    app = QApplication(sys.argv)
    main_widget = ImagesDisplayView()
    main_widget.setGeometry(100, 100, 300, 500)
    main_widget.show()

    # Random Image
    width, height = 256, 256
    random_pixels = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    image = QImage(random_pixels, width, height, QImage.Format.Format_Grayscale8)
    print(type(random_pixels))
    print(random_pixels.dtype)
    print(random_pixels.shape)
    main_widget.set_image(image)
    main_widget.set_image_from_array(random_pixels)

    sys.exit(app.exec())
