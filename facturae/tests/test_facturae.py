# -*- coding: utf-8 -*-
import unittest
from facturae.facturae_parser import FacturaeParser


class FacturaeTest(unittest.TestCase):

    def test_facturae_parser(self):
        facturae = ''
        with open('../assets/facturae.xsig', 'r') as f:
            xml_data = f.read()
            facturae = FacturaeParser(xml_data)

            self.assertEqual(facturae.sollicitud, 'F19001666A29446424')
            self.assertEqual(facturae.vat_source, 'A29446424')
            self.assertEqual(facturae.vat_destination, 'B51065928')
            self.assertEqual(facturae.num_factures, 1)
            self.assertEqual(facturae.total_factures, 92.83)
            self.assertEqual(facturae.factures[0]['InvoiceNumber'], 'F19001666')

if __name__ == '__main__':
    unittest.main()
