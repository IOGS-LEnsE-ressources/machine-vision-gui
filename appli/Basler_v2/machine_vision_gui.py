import sys
from PyQt6.QtWidgets import QApplication
from models import CameraBasler
from views import CameraView
from controllers import CameraController


def main():
    app = QApplication(sys.argv)
    model = CameraBasler()
    view = CameraView()
    controller = CameraController(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
