import pytest

from facturae.constants import XSD_MAP_VERSIONS, XSL_MAP_VERSIONS
from facturae.exceptions import AccountantValidation
from facturae.facturae_parser import FacturaeParser
from facturae.utils import FacturaeUtils
from tests.fixtures import (
    KO_INVOICE_TAX_OUTPUT,
    KO_INVOICE_TAX_WITHHELD,
    KO_INVOICE_TOTAL,
    KO_XML_V3_2_2,
)


def test_validate_invoice_tax_assert():
    parser = FacturaeParser(KO_INVOICE_TAX_OUTPUT)
    xml_obj = parser.xml_obj
    with pytest.raises(
        AssertionError, match=r".*[\"TaxesOutputs\", \"TaxesWithheld\"].*"
    ):
        parser._sum_tax_amount(xml_obj.find("Invoices"))


def test_validate_invoice_gross_amount():
    parser = FacturaeParser(KO_XML_V3_2_2)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_gross_amount(invoice)


def test_validate_invoice_tax_output():
    parser = FacturaeParser(KO_INVOICE_TAX_OUTPUT)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_tax_output(invoice)


def test_validate_invoice_tax_withheld():
    parser = FacturaeParser(KO_INVOICE_TAX_WITHHELD)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_tax_withheld(invoice)


def test_validate_invoice_total():
    parser = FacturaeParser(KO_INVOICE_TOTAL)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_total(invoice)


def test_validate_total_outstanding_amount():
    parser = FacturaeParser(KO_INVOICE_TOTAL)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_total_outstanding_amount(invoice)


def test_validate_tax_currency_code():
    parser = FacturaeParser(KO_XML_V3_2_2)
    xml_obj = parser.xml_obj

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_tax_currency_code(invoice)
