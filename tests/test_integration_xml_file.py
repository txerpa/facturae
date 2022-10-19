import pytest

from facturae.accountant_validation import InvoiceValidation
from facturae.exceptions import AccountantValidation
from tests import get_xml_obj__parser


def test_validate_invoice_total():
    path = "fixtures/accountatn_validation/KO_invoice_total.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            InvoiceValidation.validate_invoice_total(invoice)


def test_validate_total_outstanding_amount():
    path = "fixtures/accountatn_validation/KO_invoice_total.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            InvoiceValidation.validate_total_outstanding_amount(invoice)


def test_validate_tax_currency_code():
    path = "fixtures/accountatn_validation/KO_xml_v3_2_2.xml"
    xml_obj, parser = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            InvoiceValidation.validate_tax_currency_code(invoice)


def test_validate_invoice_tax_output():
    path = "fixtures/accountatn_validation/KO_invoice_tax_output.xml"
    xml_obj, _ = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            InvoiceValidation.validate_invoice_tax_output(invoice)


def test_validate_invoice_tax_withheld():
    path = "fixtures/accountatn_validation/KO_invoice_tax_withheld.xml"
    xml_obj, _ = get_xml_obj__parser(path)

    with pytest.raises(AccountantValidation):
        for invoice in xml_obj.find("Invoices").iterfind("Invoice"):
            InvoiceValidation.validate_invoice_tax_withheld(invoice)
