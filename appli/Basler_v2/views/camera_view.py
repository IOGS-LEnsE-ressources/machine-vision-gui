from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np


class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basler Camera - MVC Demo")
        self.resize(1200, 600)

        layout = QHBoxLayout(self)

        # --- Zone menu
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_quit = QPushButton("Quit")

        menu_layout = QVBoxLayout()
        menu_layout.addWidget(self.btn_start)
        menu_layout.addWidget(self.btn_stop)
        menu_layout.addStretch()
        menu_layout.addWidget(self.btn_quit)

        # --- Zone image
        self.label_image = QLabel("Flux caméra")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Zone histogramme
        self.plot_widget = pg.PlotWidget(title="Histogramme")
        self.plot_widget.setLabel("left", "Pixels")
        self.plot_widget.setLabel("bottom", "Intensité")
        self.hist_curve = self.plot_widget.plot(stepMode=True, fillLevel=0, brush=(100, 100, 200, 150))

        # --- Placement
        layout.addLayout(menu_layout, 1)
        layout.addWidget(self.label_image, 4)
        layout.addWidget(self.plot_widget, 3)

    def update_image(self, frame: np.ndarray):
        if frame.ndim == 2:
            h, w = frame.shape
            qimg = QImage(frame.data, w, h, w, QImage.Format.Format_Grayscale8)
        else:
            h, w, ch = frame.shape
            qimg = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888).rgbSwapped()

        self.label_image.setPixmap(QPixmap.fromImage(qimg).scaled(
            self.label_image.width(), self.label_image.height(), Qt.AspectRatioMode.KeepAspectRatio
        ))

    def update_histogram(self, frame: np.ndarray):
        hist, bins = np.histogram(frame, bins=256, range=(0, 255))
        self.hist_curve.setData(bins, hist, stepMode=True, fillLevel=0, brush=(100, 100, 200, 150))
    
    def closeEvent(self, event):
        QApplication.quit()
