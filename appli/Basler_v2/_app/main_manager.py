import os
from lensepy import translate
import xml.etree.ElementTree as ET
import _app.app_utils as utils

class MainManager:
    """
    Main widget/application manager.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.xml_app = None     # XML file containing application parameters
        self.list_modules = []  # List of the required modules
        self.list_main_menu = []    # Name of the modules to display in the main menu

    def set_xml_app(self, xml_app):
        """

        :param xml_app:     Filepath of the XML file containing app parameters.
        :return:    True if file exists, else False.
        """
        if os.path.exists(xml_app):
            self.xml_app = xml_app
            self.init_main_menu()
            return True
        else:
            return False

    def init_main_menu(self):
        if self.xml_app is not None:
            print(f'FP = {self.xml_app}')
            self.list_modules = self._get_list_modules()
            for module in self.list_modules:
                print(self._get_module_xml(module))
                menu_value = utils.get_subparameter_xml(self.xml_app, module, 'name')
                print(f'\tMV = {menu_value}')
                self.list_main_menu.append(menu_value)
            print(self.list_modules)
            print(self.list_main_menu)
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
        modules_list = []
        if self.xml_app is not None:
            tree = ET.parse(self.xml_app)
            xml_root = tree.getroot()
            modules = xml_root.findall('module')
            for module in modules:
                modules_list.append(module.find('name').text)
        return modules_list

    def _get_module_xml(self, module):
        """
        Get information of a module.
        :param parameter:   Name of the module inside the XML file
        :return:        Name of the module
        """
        if self.xml_app is not None:
            tree = ET.parse(self.xml_app)
            xml_root = tree.getroot()
            modules = xml_root.findall('module')
            for module_ in modules:
                if module_.find('name').text == module:
                    return module_.find('name').text, translate(f'{module_.find('name').text}_menu')
            return None, None
        else:
            return None, None