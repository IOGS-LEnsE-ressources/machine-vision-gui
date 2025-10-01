import os
from _app.app_utils import XMLFileConfig
from _app.main_view import MainWindow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from machine_vision_gui import My_Application


class MainManager:
    """
    Main widget/application manager.
    """
    def __init__(self, parent=None):
        self.parent: My_Application = parent
        self.main_window: MainWindow = MainWindow(self)
        self.xml_app: XMLFileConfig = None     # XML file containing application parameters
        self.list_modules = []  # List of the required modules
        self.main_menu_button = []
        self.app_title = ''
        self.app_logo = ''

    def set_xml_app(self, xml_app):
        """

        :param xml_app:     Filepath of the XML file containing app parameters.
        :return:    True if file exists, else False.
        """
        if os.path.exists(xml_app):
            self.xml_app = XMLFileConfig(xml_app)
            self.app_logo = self.xml_app.get_parameter_xml('logo') or ''
            self.init_main_menu()
            return True
        else:
            return False

    def init_main_menu(self):
        self.main_menu_button = []
        if self.xml_app is not None:
            self.list_modules = self._get_list_modules()
            self.main_window.set_menu_elements(self.list_modules)
            return True
        else:
            return False

    def init_views(self):
        pass

    def _get_list_modules(self):
        """
        Get a list of modules to include in the application.
        :return:
        """
        modules_list = self.xml_app.get_list_modules()
        return modules_list
