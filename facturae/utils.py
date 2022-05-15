# -*- coding: utf-8 -*-
import os
from lxml import etree
from xml.etree import ElementTree
from OpenSSL import crypto
from signxml import XMLSigner
import logging

_logger = logging.getLogger(__name__)


class FacturaeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FacturaeValidationError(FacturaeError):
    pass


class FacturaeSignError(FacturaeError):
    pass


class FacturaeUtils(object):

    @staticmethod
    def validate_xml(xml_string):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../xsd/Facturaev3_2_1.xsd")
        facturae_schema = etree.XMLSchema(
            etree.parse(open(path, 'r'))
        )
        try:
            facturae_schema.assertValid(etree.fromstring(xml_string))
        except Exception as e:
            raise FacturaeValidationError('The XML is not valid against the official XML schema definition. '
                                          'Produced error: %s' % str(e))

    @staticmethod
    def sign(xml_string, certificate, private_key):
        root = ElementTree.fromstring(xml_string)
        signed_root = XMLSigner().sign(root, key=private_key, cert=certificate)
        string_signed_root = ElementTree.tostring(signed_root).replace(b"\n", b"")
        return string_signed_root

    @classmethod
    def sign_pkcs12(cls, xml, certificate, password):
        pkcs12_key, pkcs12_cert = cls.extract_from_pkcs12(pk=certificate, passwd=password)
        try:
            string_signed_root = FacturaeUtils.sign(xml, pkcs12_cert, pkcs12_key)
        except Exception as e:
            _logger.error(f'Error occurred while trying to sign facturae xml with provided certificate: {e}')
            raise FacturaeSignError('Fail to sign facturae')
        return string_signed_root

    @classmethod
    def sign_x509(cls, xml, certificate, private_key):
        """
        :param xml: str
        :param certificate: str
        :param private_key: str
        :return:
        """
        try:
            certificate = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)

            priv_key = crypto.dump_privatekey(
                crypto.FILETYPE_PEM, private_key
            )

            cert = crypto.dump_certificate(
                crypto.FILETYPE_PEM, certificate
            )
        except Exception as e:
            _logger.error(f'Error occurred while trying to load key and certificate from a X509 certificate: {e}')
            raise FacturaeSignError('Fail to load key and certificate')
        string_signed_root = FacturaeUtils.sign(xml, cert, priv_key)
        return string_signed_root

    @staticmethod
    def extract_from_pkcs12(pk, passwd):
        """
        Return the key and the cert from a PKCS12
        """

        assert pk, "PKCS12 must be provided"
        assert passwd, "Passwd must be provided"

        try:
            p12 = crypto.load_pkcs12(pk, passwd)

            priv_key = crypto.dump_privatekey(
                crypto.FILETYPE_PEM, p12.get_privatekey()
            )

            cert = crypto.dump_certificate(
                crypto.FILETYPE_PEM, p12.get_certificate()
            )

            return priv_key, cert

        except Exception as e:
            _logger.error(f'Error occurred while trying to load key and certificate from a PKCS12 certificate: {e}')
            raise FacturaeSignError('Fail to load key and certificate')
