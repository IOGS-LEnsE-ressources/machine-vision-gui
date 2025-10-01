import sys

import _app.app_utils as utils
from PyQt6.QtWidgets import QApplication, QMainWindow
from _app.main_view import MainWindow


def main():
    utils.read_appli_XML('./config/appli.xml')
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
