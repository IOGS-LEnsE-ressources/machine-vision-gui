import sys

from _app.app_utils import XMLFileConfig
from PyQt6.QtWidgets import QApplication
from _app.main_manager import MainManager


class My_Application(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        self.manager = MainManager(self)
        self.window = self.manager.main_window
        self.config_name = './config/appli.xml'
        self.config_ok = False
        self.config = {}

    def init_config(self):
        self.config_ok = self.manager.set_xml_app(self.config_name)
        xml_data: XMLFileConfig = self.manager.xml_app
        if self.config_ok:
            self.config['name'] = xml_data.get_app_name() or None
            self.config['organization'] = xml_data.get_parameter_xml('organization') or None
            self.config['year'] = xml_data.get_parameter_xml('year') or None
            return True
        else:
            return False

    def show(self):
        # Create main window title
        title = f''
        if self.config.get('name'):
            title += f'{self.config["name"]}'
        if self.config.get('organization'):
            title += f' / {self.config["organization"]}'
        if self.config.get('year'):
            title += f' - {self.config["year"]}' or ''
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
