from contextlib import nullcontext as does_not_raise
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from facturae.accountant_validation import InvoiceValidation
from facturae.exceptions import AccountantValidation


@pytest.mark.unit
@pytest.mark.parametrize(
    "items_gross_amount, total_gross_amount, expect",
    [
        (["12.21", "2.44", "3.23"], "17.88", does_not_raise()),
        (["12.21", "2.44", "3.23"], "17.86", pytest.raises(AccountantValidation)),
        (["12.21", "2.44", "3.23"], "17.87", pytest.raises(AccountantValidation)),
    ],
)
def test_validate_invoice_gross_amount(items_gross_amount, total_gross_amount, expect):
    invoice_elem = MagicMock()
    invoice_elem.InvoiceTotals.TotalGrossAmount.text = total_gross_amount
    items_list = []
    for amount in items_gross_amount:
        items = MagicMock()
        items.GrossAmount.text = amount
        items_list.append(items)
    invoice_elem.Items.iterfind.return_value = iter(items_list)

    with expect:
        InvoiceValidation.validate_invoice_gross_amount(invoice_elem)


@pytest.mark.parametrize(
    "elem_type, taxes_amount, amount_tax, expect",
    [
        ("TaxesOutputs", ["12.21", "2.44", "3.23"], Decimal("17.88"), does_not_raise()),
        (
            "TaxesOutputs",
            ["12.21", "2.44", "3.233"],
            Decimal("17.883"),
            does_not_raise(),
        ),
        (
            "TaxesWithheld",
            ["12.21", "2.44", "3.23"],
            Decimal("17.88"),
            does_not_raise(),
        ),
        (
            "TaxesOutputs",
            ["12.21", "2.44", "3.23"],
            Decimal("17.82"),
            pytest.raises(AssertionError),
        ),
        (
            "TaxesWithheld",
            ["12.21", "2.44", "3.23"],
            Decimal("17.87"),
            pytest.raises(AssertionError),
        ),
        (
            "Fail",
            ["12.21", "2.44", "3.23"],
            Decimal("17.88"),
            pytest.raises(
                AssertionError, match=r".*[\"TaxesOutputs\", \"TaxesWithheld\"].*"
            ),
        ),
        (
            "Fail",
            ["12.21", "2.44", "3.23"],
            Decimal("17.88"),
            pytest.raises(
                AssertionError, match=r".*[\"TaxesOutputs\", \"TaxesWithheld\"].*"
            ),
        ),
    ],
)
def test_sum_tax_amount(elem_type, taxes_amount, amount_tax, expect):
    parent_elem = MagicMock()
    parent_elem.tag = elem_type
    tax_list = []
    for tax_amount in taxes_amount:
        tax = MagicMock()
        tax.TaxAmount.TotalAmount.text = tax_amount
        tax_list.append(tax)
    parent_elem.iterfind.return_value = iter(tax_list)
    with expect:
        sum_taxes = InvoiceValidation._sum_tax_amount(parent_elem)
        assert amount_tax == sum_taxes, "The sum does not add up."


@pytest.mark.parametrize(
    "sum_response, total_tax_outputs, expect",
    [
        ("17.88", "17.88", does_not_raise()),
        ("17.8832", "17.88", pytest.raises(AccountantValidation)),
        ("17.85", "17.86", pytest.raises(AccountantValidation)),
        ("17.88", "17.87", pytest.raises(AccountantValidation)),
    ],
)
def test_unit_validate_invoice_tax_output(sum_response, total_tax_outputs, expect):
    invoice_elem = MagicMock()
    invoice_elem.InvoiceTotals.TotalTaxOutputs.text = total_tax_outputs
    with expect:
        with patch.object(
            InvoiceValidation, "_sum_tax_amount", return_value=Decimal(sum_response)
        ) as mock_method:
            InvoiceValidation.validate_invoice_tax_output(invoice_elem)
            mock_method.assert_called_once()


@pytest.mark.parametrize(
    "sum_response, total_tax_withheld, expect",
    [
        ("17.88", "17.88", does_not_raise()),
        ("17.85", "17.86", pytest.raises(AccountantValidation)),
        ("17.88", "17.87", pytest.raises(AccountantValidation)),
    ],
)
def test_unit_validate_invoice_tax_withheld(sum_response, total_tax_withheld, expect):
    invoice_elem = MagicMock()
    invoice_elem.InvoiceTotals.TotalTaxesWithheld.text = total_tax_withheld
    invoice_elem.TaxesWithheld = MagicMock()
    mixin_validation = InvoiceValidation()
    with expect:
        with patch.object(
            InvoiceValidation, "_sum_tax_amount", return_value=Decimal(sum_response)
        ) as mock_method:
            mixin_validation.validate_invoice_tax_withheld(invoice_elem)
            mock_method.assert_called_once()
