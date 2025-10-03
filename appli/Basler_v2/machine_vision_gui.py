import sys
from importlib.metadata import requires

from _app.app_utils import XMLFileConfig, XMLFileModule
from PyQt6.QtWidgets import QApplication
from _app.main_manager import MainManager
import importlib
import importlib.util


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

    def init_app(self):
        self.manager.init_list_modules()

    def check_dependencies(self):
        """Check if required dependencies are installed."""
        required_modules = []
        missing_modules = []
        if self.config_ok:
            modules_list = self.manager.xml_app.get_list_modules()
            # List the missing modules
            for module in modules_list:
                module_path = self.manager.xml_app.get_module_path(module)
                if './' in module_path:
                    module_path_n = module_path.lstrip("./").replace("/", ".")
                    path_module = f'{module_path_n}.{module}'
                else:
                    path_module = f'{module_path}.{module}'
                if importlib.util.find_spec(path_module) is None:
                    missing_modules.append(module)
            # List the required modules
            for module in modules_list:
                pass
        print(f'Missing modules: {missing_modules}')
        print(f'Required modules: {required_modules}')
        if len(missing_modules) == 0 and len(required_modules) == 0:
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
        if app.check_dependencies():
            app.init_app()
            app.show()
            sys.exit(app.exec())
        else:
            print('Module dependencies failed.')
            return
    else:
        return


if __name__ == "__main__":
    main()
