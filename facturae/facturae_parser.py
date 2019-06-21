# -*- coding: utf-8 -*-
from functools import reduce
from lxml import objectify


class FacturaeParser(object):

    def __init__(self, xml_data):
        """Construir Facturae Parser"""
        self.xml_data = xml_data.encode('utf-8')
        try:
            self.xml_obj = objectify.fromstring(self.xml_data)
            self.xml_dict = self.parse_xml()
            self.sollicitud = self.xml_dict.get('BatchIdentifier', False)
            self.num_factures = self.xml_dict.get('InvoicesCount', False)
            self.total_factures = self.xml_dict.get('TotalInvoicesAmount', False)
            self.vat_source = self._get_from_dict(self.xml_dict, ['seller', 'TaxIdentificationNumber'])
            self.vat_destination = self._get_from_dict(self.xml_dict, ['buyer', 'TaxIdentificationNumber'])
            self.factures = [invoice for invoice in self.xml_dict.get('Invoices')]
        except:
            print('Something went really wrong.')

    def parse_xml(self):
        res = {}

        res.update(self.get_header_dict(self.xml_obj))
        res.update(self.get_parties_dict(self.xml_obj))
        res.update(self.get_invoices_dict(self.xml_obj))

        return res

    def get_header_dict(self, xml_obj):
        res = {}

        header = xml_obj.find('FileHeader')
        batch = header.find('Batch')

        if header:
            res.update({
                'SchemaVersion': header.SchemaVersion if header.find('SchemaVersion') else False,
                'Modality': header.Modality if header.find('Modality') else False,
                'InvoiceIssuerType': header.InvoiceIssuerType if header.find('InvoiceIssuerType') else False,
            })

        if batch:
            res.update({
                'BatchIdentifier': batch.BatchIdentifier if batch.find('BatchIdentifier') else False,
                'InvoicesCount': batch.InvoicesCount if batch.find('InvoicesCount') else False,
                'TotalInvoicesAmount': batch.TotalInvoicesAmount.TotalAmount if batch.find('TotalInvoicesAmount') else False,
                'TotalOutstandingAmount': batch.TotalOutstandingAmount.TotalAmount if batch.find('TotalOutstandingAmount') else False,
                'TotalExecutableAmount': batch.TotalExecutableAmount.TotalAmount if batch.find('TotalExecutableAmount') else False,
                'InvoiceCurrencyCode': batch.InvoiceCurrencyCode if batch.find('InvoiceCurrencyCode') else False,
            })

        return res

    def get_parties_dict(self, xml_obj):
        res = {'seller': {}, 'buyer': {}}
        parties = xml_obj.find('Parties')

        if parties:
            seller = parties.SellerParty
            buyer = parties.BuyerParty

            if seller:
                res['seller'] = self._get_party_data(seller)

            if buyer:
                res['buyer'] = self._get_party_data(buyer)

        return res

    def _get_party_data(self, party):
        res = {}

        tax_identification = party.find('TaxIdentification')
        legal_entity = party.find('LegalEntity')

        if tax_identification:
            res.update({
                'PersonTypeCode': tax_identification.PersonTypeCode if tax_identification.find('PersonTypeCode') else False,
                'ResidenceTypeCode': tax_identification.ResidenceTypeCode if tax_identification.find('ResidenceTypeCode') else False,
                'TaxIdentificationNumber': tax_identification.TaxIdentificationNumber if tax_identification.find('TaxIdentificationNumber') else False,
            })

        if legal_entity:
            res.update({
                'CorporateName': legal_entity.CorporateName if legal_entity.find('CorporateName') else False,
                'TradeName': legal_entity.TradeName if legal_entity.find('TradeName') else False,
            })

            party_address = legal_entity.find('AddressInSpain')

            if party_address:
                res.update({
                    'Address': {
                        'Street': party_address.Address if party_address.find('Address') else False,
                        'PostCode': party_address.PostCode if party_address.find('PostCode') else False,
                        'Town': party_address.Town if party_address.find('Town') else False,
                        'Province': party_address.Province if party_address.find('Province') else False,
                        'CountryCode': party_address.CountryCode if party_address.find('CountryCode') else False,
                    }
                })

        return res

    def get_invoices_dict(self, xml_obj):
        res = {'Invoices': []}
        invoices = xml_obj.find('Invoices')

        for invoice in invoices.findall('Invoice'):
            invoice_res = {}

            invoice_header = invoice.find('InvoiceHeader')
            if invoice_header:
                invoice_res.update({
                    'InvoiceNumber': invoice_header.InvoiceNumber if invoice_header.find('InvoiceNumber') else False,
                    'InvoiceDocumentType': invoice_header.InvoiceDocumentType if invoice_header.find('InvoiceDocumentType') else False,
                    'InvoiceClass': invoice_header.InvoiceClass if invoice_header.find('InvoiceClass') else False,
                })

            invoice_issue_data = invoice.find('InvoiceIssueData')
            if invoice_issue_data:
                invoice_res.update({
                    'IssueDate': invoice_issue_data.IssueDate if invoice_issue_data.find('IssueDate') else False,
                    'InvoiceCurrencyCode': invoice_issue_data.InvoiceCurrencyCode if invoice_issue_data.find('InvoiceCurrencyCode') else False,
                    'TaxCurrencyCode': invoice_issue_data.TaxCurrencyCode if invoice_issue_data.find('TaxCurrencyCode') else False,
                    'LanguageName': invoice_issue_data.LanguageName if invoice_issue_data.find('LanguageName') else False,
                })

            invoice_res.update({
                'Taxes': self._get_taxes(invoice.TaxesOutputs) if invoice.find('TaxesOutputs') else False,
            })

            invoice_totals = invoice.find('InvoiceTotals')
            if invoice_totals:
                invoice_res.update({
                    'TotalGrossAmount': invoice_totals.TotalGrossAmount if invoice_totals.find('TotalGrossAmount') else False,
                    'TotalGrossAmountBeforeTaxes': invoice_totals.TotalGrossAmountBeforeTaxes if invoice_totals.find('TotalGrossAmountBeforeTaxes') else False,
                    'TotalTaxOutputs': invoice_totals.TotalTaxOutputs if invoice_totals.find('TotalTaxOutputs') else False,
                    'TotalTaxesWithheld': invoice_totals.TotalTaxesWithheld if invoice_totals.find('TotalTaxesWithheld') else False,
                    'InvoiceTotal': invoice_totals.InvoiceTotal if invoice_totals.find('InvoiceTotal') else False,
                    'TotalOutstandingAmount': invoice_totals.TotalOutstandingAmount if invoice_totals.find('TotalOutstandingAmount') else False,
                    'TotalExecutableAmount': invoice_totals.TotalExecutableAmount if invoice_totals.find('TotalExecutableAmount') else False,
                })

            invoice_res.update({
                'IinvoiceLines': self._get_invoice_lines(invoice.Items) if invoice.find('Items') else False,
            })

            payment_details = invoice.find('PaymentDetails')
            if payment_details:
                installment = payment_details.find('Installment')
                if installment:
                    invoice_res.update({
                        'InstallmentDueDate': installment.InstallmentDueDate if installment.find(
                                'InstallmentDueDate') else False,
                        'InstallmentAmount': installment.InstallmentAmount if installment.find(
                            'InstallmentAmount') else False,
                        'PaymentMeans': installment.PaymentMeans if installment.find('PaymentMeans') else False,
                    })

                    bank_account = installment.find('AccountToBeDebited')
                    if bank_account:
                        invoice_res.update({
                            'IBAN': bank_account.IBAN if bank_account.find('IBAN') else False,
                            'BIC': bank_account.BIC if bank_account.find('BIC') else False,
                        })

            additional_data = invoice.find('AdditionalData')
            if additional_data:
                invoice_res.update({
                    'Attachments': self._get_attachments(additional_data.RelatedDocuments) if additional_data.find(
                        'RelatedDocuments') else False,
                    'InvoiceAdditionalInformation': additional_data.InvoiceAdditionalInformation if additional_data.find(
                        'InvoiceAdditionalInformation') else False,
                })

            res['Invoices'].append(invoice_res)

        return res

    def _get_taxes(self, taxes):
        res = []

        for tax in taxes.findall('Tax'):
            tax_res = {
                'TaxTypeCode': tax.TaxTypeCode if tax.find('TaxTypeCode') else False,
                'TaxRate': tax.TaxRate if tax.find('TaxRate') else False,
                'TaxableBase': tax.TaxableBase.TotalAmount if tax.find('TaxableBase') else False,
                'TaxAmount': tax.TaxAmount.TotalAmount if tax.find('TaxAmount') else False,
            }
            res.append(tax_res)

        return res

    def _get_invoice_lines(self, items):
        res = []

        for line in items.findall('InvoiceLine'):
            line_res = {
                'ItemDescription': line.ItemDescription if line.find('ItemDescription') else False,
                'Quantity': line.Quantity if line.find('Quantity') else False,
                'UnitPriceWithoutTax': line.UnitPriceWithoutTax if line.find('UnitPriceWithoutTax') else False,
                'TotalCost': line.TotalCost if line.find('TotalCost') else False,
                'GrossAmount': line.GrossAmount if line.find('GrossAmount') else False,
                'TaxesOutputs': self._get_taxes(line.TaxesOutputs) if line.find('TaxesOutputs') else False,
            }
            res.append(line_res)

        return res

    def _get_attachments(self, related_documents):
        res = []

        for attachment in related_documents.findall('Attachment'):
            attachment_res = {
                'AttachmentCompressionAlgorithm': attachment.AttachmentCompressionAlgorithm if attachment.find(
                    'AttachmentCompressionAlgorithm') else False,
                'AttachmentFormat': attachment.AttachmentFormat if attachment.find('AttachmentFormat') else False,
                'AttachmentEncoding': attachment.AttachmentEncoding if attachment.find('AttachmentEncoding') else False,
                'AttachmentData': attachment.AttachmentData if attachment.find('AttachmentData') else False,
            }
            res.append(attachment_res)

        return res

    def _get_from_dict(self,dataDict, mapList):
        """Iterate nested dictionary"""
        return reduce(dict.get, mapList, dataDict)

