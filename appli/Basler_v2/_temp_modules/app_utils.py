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


if __name__ == "__main__":
    read_appli_XML('../config/appli.xml')
