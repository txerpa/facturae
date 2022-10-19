import os

from facturae.facturae_parser import FacturaeParser


def get_xml_obj__parser(path):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
    with open(path, "rb") as f:
        parser = FacturaeParser(f.read())
        xml_obj = parser.xml_obj
    return xml_obj, parser
