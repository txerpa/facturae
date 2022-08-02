from decimal import Decimal

from facturae.constants import TaxTypeCode
from facturae.exceptions import AccountantValidation


class Validation:

    def _validate_tax(self, tax, tax_type):
        if tax.TaxTypeCode.text != tax_type:
            raise Exception("Tax error TaxTypeCode")
        tax_rate = Decimal(tax.TaxRate.text)
        total_amount = Decimal(tax.TaxableBase.TotalAmount.text)
        percentage = tax_rate / Decimal('100')
        tax_amount = total_amount * percentage
        if tax_amount != Decimal(tax.TaxAmount.TotalAmount.text):
            raise Exception("Tax error calculation")

    def _sum_taxes_amount(self, tax_type_elem, tax_type):
        sum_tax_amount = Decimal(0)
        for tax in tax_type_elem.iterfind("Tax"):
            self._validate_tax(tax, tax_type)
            sum_tax_amount += Decimal(tax.TaxAmount.TotalAmount.text)
        return sum_tax_amount

    def validate_totals(self, invoice_elem):
        invoice_total = Decimal(invoice_elem.InvoiceTotals.InvoiceTotal.text)
        total_tax_outputs = Decimal(invoice_elem.InvoiceTotals.TotalTaxOutputs.text)
        total_gross_amount = Decimal(invoice_elem.InvoiceTotals.TotalGrossAmount.text)
        total_taxes_withheld = Decimal(invoice_elem.InvoiceTotals.TotalTaxesWithheld.text)
        total_gross_amount_before_taxes = Decimal(invoice_elem.InvoiceTotals.TotalGrossAmountBeforeTaxes.text)

        sum_gross_amount = Decimal(0)
        # TotalGrossAmount
        for line_elem in invoice_elem.Items.iterfind("InvoiceLine"):
            sum_gross_amount += Decimal(line_elem.GrossAmount.text)
        if total_gross_amount != sum_gross_amount:
            raise AccountantValidation("total amount")

        # outputs
        sum_taxes_taxes_outputs = self._sum_taxes_amount(invoice_elem.TaxesOutputs,
                                                         TaxTypeCode.IVA)
        if total_tax_outputs != sum_taxes_taxes_outputs:
            raise AccountantValidation("Taxes output totals")

        # withheld
        sum_taxes_taxes_withheld = Decimal(0)
        if hasattr(invoice_elem, "TaxesWithheld"):
            sum_taxes_taxes_withheld = self._sum_taxes_amount(invoice_elem.TaxesWithheld,
                                                              TaxTypeCode.IRPF)
        if total_taxes_withheld != sum_taxes_taxes_withheld:
            raise AccountantValidation("Taxes Withheld totals")

        # TotalGrossAmount
        calculate_invoice_total = total_gross_amount_before_taxes + total_tax_outputs - total_taxes_withheld
        if invoice_total != calculate_invoice_total:
            raise AccountantValidation("TotalGrossAmountBeforeTaxes != InvoiceTotal")

        # TotalExecutableAmount
        total_executable_amount = Decimal(invoice_elem.InvoiceTotals.TotalExecutableAmount.text)
        if invoice_total != total_executable_amount:
            raise AccountantValidation("TotalExecutableAmount != InvoiceTotal")

        if total_gross_amount != total_gross_amount_before_taxes:
            raise AccountantValidation("TotalGrossAmount not equals to TotalGrossAmountBeforeTaxes")
