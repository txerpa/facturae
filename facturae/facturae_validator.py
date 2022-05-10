from lxml import etree


class FacturaeValidationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FacturaeValidator(object):

    def validate_xml(self, xml_string):
        facturae_schema = etree.XMLSchema(
            etree.parse(open('xsd/Facturaev3_2_1.xsd', 'r'))
        )
        try:
            facturae_schema.assertValid(etree.fromstring(xml_string))
        except Exception as e:
            raise FacturaeValidationError('The XML is not valid against the official XML schema definition. '
                                          'Produced error: %s' % str(e))
