import os
from _app.app_utils import XMLFileConfig, XMLFileModule
from _app.main_view import MainWindow
import importlib

from typing import TYPE_CHECKING

from modules.default.default_controller import DefaultController

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
        self.controller = None
        self.xml_app: XMLFileConfig = None     # XML file containing application parameters
        self.xml_module: XMLFileModule = None
        self.list_modules = {}
        self.list_modules_name = []      # List of the required modules
        self.actual_module = 'default'
        self.app_title = ''         # Title of the application
        self.app_logo = ''          # Logo (filepath) to display of the application
        self.variables = {}         # Application variables

    def set_xml_app(self, xml_app):
        """

        :param xml_app:     Filepath of the XML file containing app parameters.
        :return:    True if file exists, else False.
        """
        if os.path.exists(xml_app):
            self.xml_app = XMLFileConfig(xml_app)
            self.app_logo = self.xml_app.get_parameter_xml('logo') or ''
            self.app_title = self.xml_app.get_parameter_xml('appname') or ''
            if self.init_variables():
                self.list_modules_name = self.xml_app.get_list_modules()
                return self.init_main_menu()
            return False
        else:
            return False

    def init_variables(self) -> bool:
        """
        Initialize variables from application XML file.
        :return:
        """
        if self.xml_app is not None:
            self.variables = self.xml_app.get_variables()
            return True
        return False

    def init_main_menu(self):
        """
        Initialize the main menu from the module list in the application XML file.
        :return:
        """
        if self.xml_app is not None:
            self.main_window.set_menu_elements(self.list_modules_name)
            if self.actual_module == 'default':
                self.init_controller()
            return True
        else:
            return False

    def init_controller(self):
        if self.actual_module == 'default':
            xml_path = f'./modules/default/default.xml'
            self.xml_module = XMLFileModule(xml_path)
            self.controller = DefaultController(self)
        else:
            # Find controller for actual module
            module_path = self.xml_app.get_module_path(self.actual_module)
            xml_path = f'{module_path}/{self.actual_module}/{self.actual_module}.xml'
            self.xml_module = XMLFileModule(xml_path)
            controller_name = self.xml_module.get_parameter_xml('controller')
            controller_class = getattr(self.list_modules[self.actual_module], controller_name)
            self.controller = controller_class(self)
        self.controller.init_view()

    def init_list_modules(self):
        """
        Get a list of modules to include in the application.
        :return:
        """
        # Importation of modules
        for module in self.list_modules_name:
            module_path = self.xml_app.get_module_path(module)
            if './' in module_path:
                module_path_n = module_path.lstrip("./").replace("/", ".")
                self.list_modules[module] = importlib.import_module(f'{module_path_n}.{module}')
            else:
                self.list_modules[module] = importlib.import_module(f'{module_path}.{module}')


    def handle_menu_changed(self, event):
        """
        Action performed when menu changed.
            Check if the module exists
        :param event:
        """
        # Load module and initialize views
        self.actual_module = event
        self.init_controller()


