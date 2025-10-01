import sys

import _app.app_utils as utils
from PyQt6.QtWidgets import QApplication, QMainWindow
from _app.main_view import MainWindow
from _app.main_manager import MainManager


class My_Application(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        self.window = MainWindow()
        self.manager = MainManager(self)
        self.config_name = './config/appli.xml'
        self.config_ok = False
        self.config = {}

    def init_config(self):
        self.config_ok = self.manager.set_xml_app(self.config_name)
        if self.config_ok:
            self.config['name'] = utils.get_parameter_xml(self.config_name, 'name')
            self.config['organization'] = utils.get_parameter_xml(self.config_name, 'organization')
            self.config['year'] = utils.get_parameter_xml(self.config_name, 'year')
            return True
        else:
            return False


    def show(self):
        # Create main window title
        title = f''
        if self.config['name'] is not None:
            title += f'{self.config['name']}'
        if self.config['organization'] is not None:
            title += f' / {self.config['organization']}'
        if self.config['year'] is not None:
            title += f' - {self.config['year']}'
        # Display Main Window
        self.window.setWindowTitle(f'{title}')
        self.window.showMaximized()



def main():
    app = My_Application(sys.argv)
    if app.init_config():
        app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
