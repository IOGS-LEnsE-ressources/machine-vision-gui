import os
from _app.app_utils import XMLFileConfig
from _app.main_view import MainWindow
import importlib

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from machine_vision_gui import My_Application


class MainManager:
    """
    Main widget/application manager.
    """
    def __init__(self, parent=None):
        self.parent: My_Application = parent    # Parent application
        self.main_window: MainWindow = MainWindow(self)     # Main window management
        self.main_window.menu_changed.connect(self.handle_menu_changed)

        self.xml_app: XMLFileConfig = None     # XML file containing application parameters
        self.list_modules = {}
        self.list_modules_name = []      # List of the required modules
        self.actual_module = None
        self.app_title = ''         # Title of the application
        self.app_logo = ''          # Logo (filepath) to display of the application

    def set_xml_app(self, xml_app):
        """

        :param xml_app:     Filepath of the XML file containing app parameters.
        :return:    True if file exists, else False.
        """
        if os.path.exists(xml_app):
            self.xml_app = XMLFileConfig(xml_app)
            self.app_logo = self.xml_app.get_parameter_xml('logo') or ''
            self.app_title = self.xml_app.get_parameter_xml('appname') or ''
            return self.init_main_menu()
        else:
            return False

    def init_main_menu(self):
        if self.xml_app is not None:
            self.list_modules_name = self._get_list_modules()
            self.main_window.set_menu_elements(self.list_modules_name)
            return True
        else:
            return False

    def init_views(self):
        print(f'Init Views = {self.actual_module}')
        pass

    def _get_list_modules(self):
        """
        Get a list of modules to include in the application.
        :return:
        """
        modules_list = self.xml_app.get_list_modules()
        # Importation of modules
        for module in modules_list:
            module_path = self.xml_app.get_module_path(module)
            if './' in module_path:
                module_path_n = module_path.lstrip("./").replace("/", ".")
                self.list_modules[module] = importlib.import_module(f'{module_path_n}.{module}')
            else:
                self.list_modules[module] = importlib.import_module(f'{module_path}.{module}')
        return modules_list

    def handle_menu_changed(self, event):
        """
        Action performed when menu changed.
            Check if the module exists
        :param event:
        """
        # Load module and initialize views
        self.actual_module = event
        self.init_views()


