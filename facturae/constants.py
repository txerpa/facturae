
XSD_MAP_VERSIONS = (
    ("3.2.1", "3_2_1"),
    ("3.2.2", "3_2_2")
)

XSL_MAP_VERSIONS = (
    ("3.2", "32"),
    ("3.2.1", "321"),
    ("3.2.2", "322")
)

VERSION_3_2_2 = "3.2.2"

DEFAULT_VERSION = VERSION_3_2_2

POLICY_ENDPOINT = (
        "politica_de_firma_formato_facturae/"
        "politica_de_firma_formato_facturae_v3_1"
        ".pdf"
    )

SIGN_POLICY = f"http://www.facturae.es/{POLICY_ENDPOINT}"

SIGNER_ROLE = (
    "supplier",
    "emisor",
    "customer",
    "receptor",
    "third party",
    "tercero"
)

# Modality
MODALITY_SINGLE = 'I'
MODALITY_BATCH = 'L'


class InvoiceClass:
    ORIGINAL = 'OO'
    ORIGINAL_CORRECTIVE = 'OR'
    ORIGINAL_SUMMARY = 'OC'
    ORIGINAL_DUPLICATED = 'CO'
    CORRECTIVE_DUPLICATED = 'CR'
    SUMMARY_DUPLICATED = 'CC'


class InvoiceDocumentType:
    COMPLETE_INVOICE = 'FC'
    ABBREVIATED = 'FA'
    SELF_INVOICE = 'AF'


class InvoiceIssuerType:
    SELLER = 'EM'
    BUYER = 'RE'
    THIRD_PARTY = 'TE'


class CorrectiveInvoiceReasonCode:
    """Código numérico del motivo de rectificación"""
    INVOICE_NUMBER = '01'
    INVOICE_SERIAL_NUMBER = '02'
    ISSUE_DATE = '03'
    ISSUERS_NAME = '04'
    RECEIVERS_NAME = '05'
    ISSUERS_NIF = '06'
    RECEIVERS_NIF = '07'
    ISSUERS_ADDRESS = '08'
    RECEIVERS_ADDRESS = '09'
    ITEM_LINE = '10'
    APPLICABLE_TAX_RATE = '11'
    APPLICABLE_TAX_AMOUNT = '12'
    APPLICABLE_DATE = '13'
    INVOICE_CLASS = '14'
    LEGAL_LITERALS = '15'
    TAXABLE_BASE = '16'
    CALCULATION_OF_TAX_OUTPUTS = '80'
    CALCULATION_OF_TAX_INPUTS = '81'
    TAXABLE_BASE_MODIFIES_DUE_PACKAGE_RETURN = '82'
    TAXABLE_BASE_MODIFIES_DUE_DISCOUNTS = '83'
    TAXABLE_BASE_MODIFIES_DUE_FIRM_COURT_RULING = '84'
    TAXABLE_BASE_MODIFIES_DUE_UNPAID_OUTPUTS = '85'

    DESCRIPTION = {
        INVOICE_NUMBER: 'Número de la factura',
        INVOICE_SERIAL_NUMBER: 'Serie de la factura',
        ISSUE_DATE: 'Fecha expedición',
        ISSUERS_NAME: 'Nombre y apellidos/Razón Social-Emisor',
        RECEIVERS_NAME: 'Nombre y apellidos/Razón Social-Receptor',
        ISSUERS_NIF: 'Identificación fiscal Emisor/obligado',
        RECEIVERS_NIF: 'Identificación fiscal Receptor',
        ISSUERS_ADDRESS: 'Domicilio Emisor/Obligado',
        RECEIVERS_ADDRESS: 'Domicilio Receptor',
        ITEM_LINE: 'Detalle Operación',
        APPLICABLE_TAX_RATE: 'Porcentaje impositivo a aplicar',
        APPLICABLE_TAX_AMOUNT: 'Cuota tributaria a aplicar',
        APPLICABLE_DATE: 'Fecha/Periodo a aplicar',
        INVOICE_CLASS: 'Clase de factura',
        LEGAL_LITERALS: 'Literales legales',
        TAXABLE_BASE: 'Base imponible',
        CALCULATION_OF_TAX_OUTPUTS: 'Cálculo de cuotas repercutidas',
        CALCULATION_OF_TAX_INPUTS: 'Cálculo de cuotas retenidas',
        TAXABLE_BASE_MODIFIES_DUE_PACKAGE_RETURN: 'Base imponible modificada por devolución de envases / embalajes',
        TAXABLE_BASE_MODIFIES_DUE_DISCOUNTS: 'Base imponible modificada por descuentos y bonificaciones',
        TAXABLE_BASE_MODIFIES_DUE_FIRM_COURT_RULING: 'Base imponible modificada por resolución firme, judicial o administrativa',
        TAXABLE_BASE_MODIFIES_DUE_UNPAID_OUTPUTS: 'Base imponible modificada cuotas repercutidas no satisfechas. Auto de declaración de concurso',
    }


class CorrectionMethodType:
    """Numerical code to identify the method applied to correct an invoice."""
    FULL_ITEMS = '01'
    CORRECTED_ITEMS_ONLY = '02'
    BULK_DEAL = '03'
    AUTHORIZED_BY_TAX_AGENCY = '04'

    DESCRIPTION = {
        FULL_ITEMS: 'Rectificación íntegra',
        CORRECTED_ITEMS_ONLY: 'Rectificación por diferencias',
        BULK_DEAL: 'Rectificación por descuento por volumen de operaciones durante un periodo',
        AUTHORIZED_BY_TAX_AGENCY: 'Autorizadas por la Agencia Tributaria',
    }


class ResidenceTypeCode:
    """It identifies whether the person is resident or non-resident"""
    FOREIGN = 'E'
    RESIDENT = 'R'
    EU_RESIDENT = 'U'


# Person Type Code
PERSON_TYPE_PHYSICAL = 'F'
PERSON_TYPE_JURIDICAL = 'J'

# Tax Type Code
# Name of the chargeable tax or the tax applicable to the amounts withheld.
TAX_VALUE_ADDED = '01'
TAX_IRPF = '04'
TAX_OTHER = '05'

# Payment Means Type
# Each installment may be paid using a specific payment means
PAYMENT_MEANS_IN_CASH = '01'
PAYMENT_MEANS_DIRECT_DEBIT = '02'
PAYMENT_MEANS_CREDIT_TRANSFER = '04'
PAYMENT_MEANS_SPECIAL = '13'
PAYMENT_MEANS_CARD = '19'