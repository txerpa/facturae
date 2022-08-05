import pytest

from facturae.exceptions import AccountantValidation
from tests import get_xml_obj__parser


def test_validate_invoice_tax_assert():
    path = "fixtures/accountatn_validation/KO_invoice_tax_output.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(
        AssertionError, match=r".*[\"TaxesOutputs\", \"TaxesWithheld\"].*"
    ):
        parser._sum_tax_amount(xml_obj.find("Invoices"))


def test_validate_invoice_gross_amount():
    path = "fixtures/accountatn_validation/KO_xml_v3_2_2.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_gross_amount(invoice)


def test_validate_invoice_tax_output():
    path = "fixtures/accountatn_validation/KO_invoice_tax_output.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_tax_output(invoice)


def test_validate_invoice_tax_withheld():
    path = "fixtures/accountatn_validation/KO_invoice_tax_withheld.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_tax_withheld(invoice)


def test_validate_invoice_total():
    path = "fixtures/accountatn_validation/KO_invoice_total.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_invoice_total(invoice)


def test_validate_total_outstanding_amount():
    path = "fixtures/accountatn_validation/KO_invoice_total.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_total_outstanding_amount(invoice)


def test_validate_tax_currency_code():
    path = "fixtures/accountatn_validation/KO_xml_v3_2_2.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            parser.validate_tax_currency_code(invoice)
