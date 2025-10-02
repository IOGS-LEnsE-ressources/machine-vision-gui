import sys, os
import xml.etree.ElementTree as ET


class XMLFileConfig:

    def __init__(self, xml_file: str):
        """

        :param xml_file:    File path of the XML file.
        """
        if os.path.isfile(xml_file):
            self.xml_file = xml_file
        else:
            self.xml_file = None

    def get_parameter_xml(self, parameter):
        """

        :param parameter:   Name of the node inside the XML file.
        :return:        Value of the parameter.
        """
        if self.xml_file is not None:
            tree = ET.parse(self.xml_file)
            xml_root = tree.getroot()
            param_value = xml_root.find(parameter)
            if param_value is not None:
                return param_value.text
        return None

    def get_app_name(self):
        """

        :return:    Name of the application from the XML file.
        """
        return self.get_parameter_xml('name')

    def get_list_modules(self):
        """

        :return:
        """
        modules_list = []
        if self.xml_file is not None:
            tree = ET.parse(self.xml_file)
            xml_root = tree.getroot()
            modules = xml_root.findall('module')
            for module in modules:
                modules_list.append(module.find('name').text)
        return modules_list

    def get_module_path(self, module_name: str):
        """

        :param module_name: Name of the module
        :return:
        """
        modules_list = []
        if self.xml_file is not None:
            tree = ET.parse(self.xml_file)
            xml_root = tree.getroot()
            modules = xml_root.findall('module')
            for module in modules:
                if module.find('name').text == module_name:
                    return module.find('location').text
        return None

    def get_xml_file(self):
        """

        :return:
        """
        return self.xml_file



if __name__ == "__main__":
    pass
