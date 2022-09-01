import inspect
from decimal import Decimal

from facturae.constants import TaxTypeCode
from facturae.exceptions import AccountantValidation


class InvoiceValidation:
    @staticmethod
    def run_all_validations(invoice_elem):
        for name, func in dict(
            inspect.getmembers(InvoiceValidation, predicate=inspect.isfunction)
        ).items():
            if name.startswith("validate_"):
                print(func)
                func(invoice_elem)

    @staticmethod
    def _sum_tax_amount(parent_elem):
        """
        Sum tax amount from TaxesOutputs or TaxesWithheld
        """
        valid_parents = ["TaxesOutputs", "TaxesWithheld"]
        assert (
            parent_elem.tag in valid_parents
        ), f"Parent elem must be one of {valid_parents}"

        num_decimals = 0
        list_taxes = []
        for tax in parent_elem.iterfind("Tax"):
            amount = Decimal(tax.TaxAmount.TotalAmount.text)
            list_taxes.append(amount)
            decimals = abs(amount.as_tuple().exponent)
            if decimals > num_decimals:
                num_decimals = decimals
        return sum(list_taxes).__round__(num_decimals) or Decimal(0)

    @staticmethod
    def validate_invoice_gross_amount(invoice_elem):
        sum_gross_amount = Decimal(0)
        total_gross_amount = Decimal(invoice_elem.InvoiceTotals.TotalGrossAmount.text)

        for line_elem in invoice_elem.Items.iterfind("InvoiceLine"):
            sum_gross_amount += Decimal(line_elem.GrossAmount.text)
        if total_gross_amount != sum_gross_amount:
            raise AccountantValidation("total amount")

    @staticmethod
    def validate_invoice_tax_output(invoice_elem):
        total_tax_outputs = Decimal(invoice_elem.InvoiceTotals.TotalTaxOutputs.text)
        sum_taxes_taxes_outputs = InvoiceValidation._sum_tax_amount(
            invoice_elem.TaxesOutputs
        )
        if total_tax_outputs != sum_taxes_taxes_outputs:
            raise AccountantValidation("Taxes output totals")

    @staticmethod
    def validate_invoice_tax_withheld(invoice_elem):
        total_taxes_withheld = Decimal(
            invoice_elem.InvoiceTotals.TotalTaxesWithheld.text
        )
        sum_taxes_taxes_withheld = Decimal(0)
        if hasattr(invoice_elem, "TaxesWithheld"):
            sum_taxes_taxes_withheld = InvoiceValidation._sum_tax_amount(
                invoice_elem.TaxesWithheld
            )
        if total_taxes_withheld != sum_taxes_taxes_withheld:
            raise AccountantValidation("Taxes Withheld totals")

    @staticmethod
    def validate_invoice_total(invoice_elem):
        invoice_total = Decimal(invoice_elem.InvoiceTotals.InvoiceTotal.text)
        total_tax_outputs = Decimal(invoice_elem.InvoiceTotals.TotalTaxOutputs.text)
        total_taxes_withheld = Decimal(
            invoice_elem.InvoiceTotals.TotalTaxesWithheld.text
        )
        total_gross_amount_before_taxes = Decimal(
            invoice_elem.InvoiceTotals.TotalGrossAmountBeforeTaxes.text
        )
        calculate_invoice_total = (
            total_gross_amount_before_taxes + total_tax_outputs - total_taxes_withheld
        )
        if invoice_total != calculate_invoice_total:
            invoice_num = invoice_elem.InvoiceHeader.InvoiceNumber.text
            raise AccountantValidation(
                f"Error en la factura nº{invoice_num}. "
                f'Desde el elemento "InvoiceTotals", '
                f'"InvoiceTotal" (InvoiceTotals/InvoiceTotal) no es igual a '
                f'"TotalGrossAmountBeforeTaxes" (TotalImporteBrutoAntesImpuestos ) + '
                f'"TotalTaxOutputs" (TotalImpuestosRepercutidos) - '
                f'"TotalTaxesWithheld" (TotalImpuestosRetenidos)'
            )

    @staticmethod
    def validate_total_outstanding_amount(invoice_elem):

        total_outstanding_amount = Decimal(
            invoice_elem.InvoiceTotals.TotalOutstandingAmount.text
        )

        # Subsidies
        subsidies_sum = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "Subsidies"):
            subsidies_sum = sum(
                map(
                    lambda Subsidy: Decimal(Subsidy.SubsidyAmount.text),
                    invoice_elem.InvoiceTotals.Subsidies.iterfind("Subsidy"),
                )
            ) or Decimal(0)

        # TotalPaymentsOnAccount
        total_payments_on_account = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "TotalPaymentsOnAccount"):
            total_payments_on_account = Decimal(
                invoice_elem.InvoiceTotals.TotalPaymentsOnAccount.text
            )

        invoice_total = Decimal(invoice_elem.InvoiceTotals.InvoiceTotal.text)
        calc_total_outstanding_amount = (
            invoice_total - subsidies_sum + total_payments_on_account
        )
        if calc_total_outstanding_amount != total_outstanding_amount:
            invoice_num = invoice_elem.InvoiceHeader.InvoiceNumber.text
            raise AccountantValidation(
                f"Error en la factura nº{invoice_num}. "
                f'Desde el elemento "Invoice Totals", '
                f'"TotalOutstandingAmount" (Total a Pagar) no es igual a '
                f'"InvoiceTotal" (Total Factura ) + '
                f'"Sum Subsidy" (Sumatorio de Importe Subvencion) - '
                f'"TotalPaymentsOnAccount" (Total Anticipos)'
            )

    @staticmethod
    def validate_total_executable_amount(invoice_elem):
        total_executable_amount = Decimal(
            invoice_elem.InvoiceTotals.TotalExecutableAmount.text
        )

        amounts_withheld = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "AmountsWithheld"):
            amounts_withheld = Decimal(
                invoice_elem.InvoiceTotals.AmountsWithheld.WithholdingAmount.text
            )
        payment_in_kind_amount = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "PaymentInKind"):
            payment_in_kind_amount = Decimal(
                invoice_elem.InvoiceTotals.PaymentInKind.PaymentInKindAmount.text
            )
        total_financial_expenses = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "TotalFinancialExpenses"):
            total_financial_expenses = Decimal(
                invoice_elem.InvoiceTotals.TotalFinancialExpenses.text
            )

        total_reimbursable_expenses = Decimal(0)
        if hasattr(invoice_elem.InvoiceTotals, "TotalReimbursableExpenses"):
            total_reimbursable_expenses = Decimal(
                invoice_elem.InvoiceTotals.TotalReimbursableExpenses.text
            )

        total_outstanding_amount = Decimal(
            invoice_elem.InvoiceTotals.TotalOutstandingAmount.text
        )

        calc_total_executable_amount = (
            total_outstanding_amount
            - amounts_withheld
            - payment_in_kind_amount
            + total_reimbursable_expenses
            + total_financial_expenses
        )

        if calc_total_executable_amount != total_executable_amount:
            invoice_num = invoice_elem.InvoiceHeader.InvoiceNumber.text
            raise AccountantValidation(
                f"Error en la factura nº{invoice_num}. "
                f'Desde el elemento "InvoiceTotals", '
                f"TotalExecutableAmount (Total a ejecutar). Es el Resultado de: "
                f'"TotalOutstandingAmount" (Total a Pagar ) - '
                f'"AmountsWithheld" (Total de Cantidades retenidas ) - '
                f'"PaymentInKindAmount" (Importe Pago en Especie ) + '
                f'"TotalReimbursableExpenses" (Total Suplidos ) + '
                f'"TotalFinancialExpenses" (Total Gastos Financieros ). \n'
                f"En Total de Cantidades retenidas se sumaran las cantidades"
                f"especificadas en los bloques AmountsWithheld"
                ""
            )

    @staticmethod
    def validate_tax_currency_code(invoice_elem):
        if invoice_elem.InvoiceIssueData.TaxCurrencyCode != "EUR":
            raise AccountantValidation(
                "El nodo MonedaImpuesto(TaxCurrencyCode) debe ser obligatoriamente EUR"
            )

    # LOTE

    # todo:
    """
    El importe total de TotalFacturas(Batch/TotalInvoicesAmount/TotalAmount) del lote no coincide con la
    suma de los importes de cada factura, deberia ser : 2207.5

    ??EquivalentInEuros
    """

    # todo
    """
    El importe total de TotalAPagar del lote no coincide con la suma de los
    importes de cada factura, deberia ser : 2207.

    Total a pagar. Suma de los importes
    TotalOutstandingAmount del Fichero. Es el importe que

    ??EquivalentInEuros
    """

    # todo
    """
    El importe total de TotalAEjecutar del lote no coincide con la suma de los
    importes de cada factura, deberia ser : 2207.5

    Total a Ejecutar. Sumatorio de los Importes
    TotalExecutableAmount del fichero.
    """

    # todo
    """
    La moneda de facturación no es EURO y no se ha indicado la equivalencia
    en euros para
    Batch
    * TotalInvoicesAmount
    * TotalOutstandingAmount
    * TotalExecutableAmount
    """

    ## invoice line
    # todo
    """
    InvoiceIssueData/InvoiceCurrencyCode
    La moneda de la factura no es EURO y no se ha indicado la equivalencia
    en euros para la base imponible de
    A nivel de Invoice-line
    ImpuestosRetenidos (TotalTaxesWithheld) --> EquivalentInEuros
    ImpuestosRepercutidos (TaxesOutputs) --> EquivalentInEuros

    A nivel de Invoice
    ImpuestosRetenidos (TotalTaxesWithheld) --> EquivalentInEuros
    ImpuestosRepercutidos (TaxesOutputs) --> EquivalentInEuros
    """

    # Invoice
    # todo
    """
     El nodo MonedaImpuesto(TaxCurrencyCode) debe ser obligatoriamente EUR
    """
