XSD_MAP_VERSIONS = (("3.2.1", "3_2_1"), ("3.2.2", "3_2_2"))

XSL_MAP_VERSIONS = (("3.2", "32"), ("3.2.1", "321"), ("3.2.2", "322"))

VERSION_3_2_2 = "3.2.2"

DEFAULT_VERSION = VERSION_3_2_2

POLICY_ENDPOINT = (
    "politica_de_firma_formato_facturae/"
    "politica_de_firma_formato_facturae_v3_1"
    ".pdf"
)

SIGN_POLICY = f"http://www.facturae.es/{POLICY_ENDPOINT}"

SIGNER_ROLE = ("supplier", "emisor", "customer", "receptor", "third party", "tercero")


class MODALITY:
    """
    Single or Batch.
    If it is "single" (I) the amounts of the fields of group Batch will match their
    corresponding fields of group InvoiceTotals and field InvoicesCount will always
    take the value "1". If it is a "batch" (L), the value of field InvoicesCount
    will always be > "1".
    """

    SINGLE = "I"  # Individual
    BATCH = "L"  # Lote


class InvoiceClass:
    """
    This piece of information states the type of invoice, that is:
        OO - Original
        OR - Corrective
        OC – Summary original
        CO – Copy of the original
        CR – Copy of the corrective
        CC – copy of the summary
    A corrective invoice can only correct an original invoice, or credit an amount due
    to volume in a deferred period, or for any other reason allowed by the Tax Agency.
    When the “type” takes the value “OR” or “CR” (correctives), fields of group Corrective
    must be filled in.
    """

    ORIGINAL = "OO"
    ORIGINAL_CORRECTIVE = "OR"
    ORIGINAL_SUMMARY = "OC"
    ORIGINAL_DUPLICATED = "CO"
    CORRECTIVE_DUPLICATED = "CR"
    SUMMARY_DUPLICATED = "CC"


class InvoiceDocumentType:
    """
    Tipo documento factura. Puede tomar 3 valores:
        FC - “Complete Invoice”
        FA - “Abbreviated.”
    """

    COMPLETE = "FC"
    ABBREVIATED = "FA"


class InvoiceDocumentType:
    COMPLETE_INVOICE = "FC"
    ABBREVIATED = "FA"
    SELF_INVOICE = "AF"


class InvoiceIssuerType:
    """
    Party who signs the invoice.
        EM - “Provider (previously called issuer)”
        RE - “Recipient (previously called client or receiver)”
        TE - “Third Party”
    If the value "TE" (Issuer type) is chosen, all sections of group ThirdParty must be filled in.
    """

    SELLER = "EM"
    BUYER = "RE"
    THIRD_PARTY = "TE"


class CorrectiveInvoiceReasonCode:
    """Código numérico del motivo de rectificación"""

    INVOICE_NUMBER = "01"
    INVOICE_SERIAL_NUMBER = "02"
    ISSUE_DATE = "03"
    ISSUERS_NAME = "04"
    RECEIVERS_NAME = "05"
    ISSUERS_NIF = "06"
    RECEIVERS_NIF = "07"
    ISSUERS_ADDRESS = "08"
    RECEIVERS_ADDRESS = "09"
    ITEM_LINE = "10"
    APPLICABLE_TAX_RATE = "11"
    APPLICABLE_TAX_AMOUNT = "12"
    APPLICABLE_DATE = "13"
    INVOICE_CLASS = "14"
    LEGAL_LITERALS = "15"
    TAXABLE_BASE = "16"
    CALCULATION_OF_TAX_OUTPUTS = "80"
    CALCULATION_OF_TAX_INPUTS = "81"
    TAXABLE_BASE_MODIFIES_DUE_PACKAGE_RETURN = "82"
    TAXABLE_BASE_MODIFIES_DUE_DISCOUNTS = "83"
    TAXABLE_BASE_MODIFIES_DUE_FIRM_COURT_RULING = "84"
    TAXABLE_BASE_MODIFIES_DUE_UNPAID_OUTPUTS = "85"

    DESCRIPTION = {
        INVOICE_NUMBER: "Número de la factura",
        INVOICE_SERIAL_NUMBER: "Serie de la factura",
        ISSUE_DATE: "Fecha expedición",
        ISSUERS_NAME: "Nombre y apellidos/Razón Social-Emisor",
        RECEIVERS_NAME: "Nombre y apellidos/Razón Social-Receptor",
        ISSUERS_NIF: "Identificación fiscal Emisor/obligado",
        RECEIVERS_NIF: "Identificación fiscal Receptor",
        ISSUERS_ADDRESS: "Domicilio Emisor/Obligado",
        RECEIVERS_ADDRESS: "Domicilio Receptor",
        ITEM_LINE: "Detalle Operación",
        APPLICABLE_TAX_RATE: "Porcentaje impositivo a aplicar",
        APPLICABLE_TAX_AMOUNT: "Cuota tributaria a aplicar",
        APPLICABLE_DATE: "Fecha/Periodo a aplicar",
        INVOICE_CLASS: "Clase de factura",
        LEGAL_LITERALS: "Literales legales",
        TAXABLE_BASE: "Base imponible",
        CALCULATION_OF_TAX_OUTPUTS: "Cálculo de cuotas repercutidas",
        CALCULATION_OF_TAX_INPUTS: "Cálculo de cuotas retenidas",
        TAXABLE_BASE_MODIFIES_DUE_PACKAGE_RETURN: "Base imponible modificada por devolución de envases / embalajes",
        TAXABLE_BASE_MODIFIES_DUE_DISCOUNTS: "Base imponible modificada por descuentos y bonificaciones",
        TAXABLE_BASE_MODIFIES_DUE_FIRM_COURT_RULING: "Base imponible modificada por resolución firme, judicial o administrativa",
        TAXABLE_BASE_MODIFIES_DUE_UNPAID_OUTPUTS: "Base imponible modificada cuotas repercutidas no satisfechas. Auto de declaración de concurso",
    }


class CorrectionMethodType:
    """
    Numerical code to identify the method applied to correct an invoice.
        "01" - all the details to rectify from the original invoice are reflected.
        "02" – only the details already rectified are noted.
        "03" - Rectification due to discount for the volume of operations during a period.
        "04" - Authorized by the Tax Agency.
    """

    FULL_ITEMS = "01"
    CORRECTED_ITEMS_ONLY = "02"
    BULK_DEAL = "03"
    AUTHORIZED_BY_TAX_AGENCY = "04"

    DESCRIPTION = {
        FULL_ITEMS: "Rectificación íntegra",
        CORRECTED_ITEMS_ONLY: "Rectificación por diferencias",
        BULK_DEAL: "Rectificación por descuento por volumen de operaciones durante un periodo",
        AUTHORIZED_BY_TAX_AGENCY: "Autorizadas por la Agencia Tributaria",
    }


class ResidenceTypeCode:
    """It identifies whether the person is resident or non-resident"""

    FOREIGN = "E"
    RESIDENT = "R"
    EU_RESIDENT = "U"


class TypePerson:
    INDIVIDUAL = "F"
    LEGAL_ENTITY = "J"


class TaxTypeCode:
    # Name of the chargeable tax or the tax applicable to the amounts withheld.
    IVA = "01"  # Impuesto sobre el valor añadido
    IPSI = "02"  # Impuesto sobre la producción, los servicios y la importación
    IGIC = "03"  # Impuesto general indirecto de Canarias
    IRPF = "04"  # Impuesto sobre la Renta de las personas físicas
    Other = "05"  # OTROS
    ITPAJD = "06"  # Impuesto sobre transmisiones patrimoniales y actos jurídicos documentados
    IE = "07"  # Impuestos especiales
    Ra = "08"  # Renta aduanas
    IGTECM = "09"  # Impuesto general sobre el tráfico de empresas que se aplica en Ceuta y Melilla
    IECDPCAC = "10"  # Impuesto especial sobre los combustibles derivados del petróleo en la Comunidad Autonoma Canaria
    IIIMAB = "11"  # Impuesto sobre las instalaciones que inciden sobre el medio ambiente en las Baleares
    ICIO = "12"  # Impuesto sobre las construcciones, instalaciones y obras
    IMVDN = "13"  # Impuesto municipal sobre las viviendas desocupadas en Navarra
    IMSN = "14"  # Impuesto municipal sobre gastos suntuarios en Navarra
    IMGSN = "15"  # Impuesto municipal sobre gastos suntuarios en Navarra
    IMPN = "16"  # Impuesto municipal sobre publicidad en Navarra
    REIVA = "17"  # Régimen especial de IVA para agencias de viajes
    REIGIC = "18"  # Régimen especial de IGIC: para agencias de viajes
    REIPSI = "19"  # Régimen especial de IPSI para agencias de viajes
    IPS = "20"  # Impuestos sobre las primas de seguros
    RLEA = "21"  # Recargo destinado a financiar las funciones de liquidación de entidades aseguradoras
    IVPEE = "22"  # Impuesto sobre el valor de la producción de la energía eléctrica
    IPCN = "23"  # Impuesto sobre la producción de combustible nuclear gastado y residuos radiactivos resultantes de la generación de energía nucleoeléctrica
    IACN = "24"  # Impuesto sobre el almacenamiento de combustible nuclear gastado y residuos radioactivos en instalaciones centralizadas
    IDEC = "25"  # Impuesto sobre los Depósitos en las Entidades de Crédito
    ILTC = "26"  # Impuesto sobre las labores del tabaco en la Comunidad Autónoma de Canarias
    IGFEI = "27"  # Impuesto sobre los Gases Fluorados de Efecto Invernadero
    IRNR = "28"  # Impuesto sobre la Renta de No Residentes
    IS = "29"  # Impuesto sobre Sociedades


# Payment Means Type
# Each installment may be paid using a specific payment means
class PaymentMeansType:
    IN_CASH = "01"  # In cash
    DIRECT_DEBIT = "02"
    RECEIPT = "03"
    CREDIT_TRANSFER = "04"
    ACCEPTED_BILL_EXCHANGE = "05"
    DOCUMENTARY_CREDIT = "06"
    CONTRACT_AWARD = "07"
    BILL_EXCHANGE = "08"
    TRANSFERABLE_PROMISSORY_NOTE = "09"
    NON_TRANSFERABLE_PROMISSORY_NOTE = "10"
    CHEQUE = "11"
    OPEN_ACCOUNT_REIMBURSEMENT = "12"
    SPECIAL = "13"
    SET_OFF_BY_RECIPROCAL_CREDITS = "14"
    POSTGIRO = "15"
    CERTIFIED_CHEQUE = "16"
    BANKERS_DRAFT = "17"
    CASH_ON_DELIVERY = "18"
    BY_CARD = "19"
