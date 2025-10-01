import sys, os
import xml.etree.ElementTree as ET


def read_appli_XML(filepath: str):
    """

    :param filepath:    Name of the XML file containing application parameters
    :return:    List of all the nodes of the XML file
    """
    # Open the file
    if os.path.exists(filepath):
        tree = ET.parse(filepath)
        xml_root = tree.getroot()

        # Name of the xml root
        print(f'Root name : {xml_root.tag}')
        print(f'App name : {xml_root.get("name")}')

        modules = xml_root.findall("module")
        if len(modules) > 0:
            print(f"{len(modules)} noeud(s) 'module' trouvé(s).")

        for module in modules:
            print(f'{module.find("name").text}')

    else:
        return None


def get_parameter_xml(filepath, parameter):
    """

    :param filepath:    Path to the XML file
    :param parameter:   Name of the node inside the XML file
    :return:        Value of the parameter
    """
    tree = ET.parse(filepath)
    xml_root = tree.getroot()
    param_value = xml_root.find(parameter)
    if param_value is not None:
        return param_value.text
    else:
        return None

def get_subparameter_xml(filepath, parameter, subparameter):
    """

    :param filepath:    Path to the XML file
    :param parameter:   Name of the node inside the XML file
    :param subparameter:    Name of the subnode inside the XML file
    :return:        Value of the sub-parameter
    """
    print(filepath)
    tree = ET.parse(filepath)
    xml_root = tree.getroot()
    param_value = xml_root.find(parameter)
    print(f'PP = {param_value}')
    if param_value is not None:
        print(param_value.text)
        sub_value = param_value.find(subparameter)
        print(f'TT = {sub_value}')
        if sub_value is not None:
            return sub_value.text
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    read_appli_XML('../config/appli.xml')
