# -*- coding: utf-8 -*-
import os
import xmlsig
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from .constants import XSD_MAP_VERSIONS, XSL_MAP_VERSIONS, DEFAULT_VERSION, \
    SIGN_POLICY, SIGNER_ROLE

from lxml import etree
from xml.etree import ElementTree
from OpenSSL import crypto
from signxml import XMLSigner
from xades import utils, template, XAdESContext
from xades.policy import GenericPolicyId
import logging

from facturae.exceptions import FacturaeSignError, FacturaeValidationError

_logger = logging.getLogger(__name__)


class FacturaeUtils(object):

    @staticmethod
    def get_xsd_file(version):
        mapped_versions = dict(XSD_MAP_VERSIONS)
        _version = mapped_versions[version]
        return f"../xsd/Facturaev{_version}.xsd"

    @staticmethod
    def get_xsl_file(version):
        mapped_versions = dict(XSL_MAP_VERSIONS)
        _version = mapped_versions[version]
        return f"../xsl/Visualizador{_version}.xsl"

    @staticmethod
    def validate_xml(xml_string, version=None):
        version = version or DEFAULT_VERSION
        xsd_file_name = FacturaeUtils.get_xsd_file(version)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), xsd_file_name)
        _logger.debug(f"XSD: {path}")
        facturae_schema = etree.XMLSchema(
            etree.parse(open(path, 'r'))
        )
        try:
            facturae_schema.assertValid(etree.fromstring(xml_string))
        except Exception as e:
            raise FacturaeValidationError(
                'The XML is not valid against the official '
                'XML schema definition. Produced error: %s' % str(e))

    @staticmethod
    def to_html(xml_string, version):
        xsl_file = FacturaeUtils.get_xsl_file(version)
        xsl_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), xsl_file)
        _logger.debug(f"XSL: {xsl_path}")
        with open(xsl_path, "rb") as f:
            xslt_root = etree.parse(f)
        transform = etree.XSLT(xslt_root)
        result = transform(etree.XML(xml_string))
        return bytes(result)  # html

    @staticmethod
    def sign_xmldsig(xml_string, certificate, private_key):
        """
        Sign xml document using basic XML signature, defined in XML-DSig standard
        """
        root = ElementTree.fromstring(xml_string)
        signed_root = XMLSigner().sign(root, key=private_key, cert=certificate)
        string_signed_root = ElementTree.tostring(signed_root).replace(b"\n", b"")
        return string_signed_root

    @staticmethod
    def sign_xades(xml: str, public_cert: str, private_key: str,
                   signer_role: str = None,
                   signature_production_place: dict = None):
        """
        Apply XADES-EPES signature to XML
        :param xml: XML to sign
        :param public_cert: Path to certificate file
        :param private_key: Path to private key file
        :param signer_role: Role of the signer. Optional.
        Has to be one of the role defined in SIGNER_ROLE
        :param signature_production_place: Optional. dict with following keys:
            'state': signature production province,
            'city': signature production city,
            'postal_code': signature production postal code,
            'country': signature production country
        :return: Signed xml in str format
        """
        # Parse file we want to sign
        parsed_file = etree.fromstring(xml)
        # Create Signature template with the corresponding Transform stuff
        signature = xmlsig.template.create(
            xmlsig.constants.TransformInclC14N,
            xmlsig.constants.TransformRsaSha1,
            "Signature",
        )
        # Create an uuid and the reference to the signature
        signature_id = utils.get_unique_id()
        ref = xmlsig.template.add_reference(
            signature, xmlsig.constants.TransformSha1, uri="", name="REF"
        )
        # Create transform for the signature reference
        xmlsig.template.add_transform(ref, xmlsig.constants.TransformEnveloped)
        # 5.Add the other references
        xmlsig.template.add_reference(
            signature, xmlsig.constants.TransformSha1,
            uri="#" + signature_id,
            uri_type="http://uri.etsi.org/01903/v1.2.2#SignedProperties"
        )
        key_info_id = utils.get_unique_id()
        xmlsig.template.add_reference(
            signature, xmlsig.constants.TransformSha1, uri="#" + key_info_id
        )
        # Add the part where the certificate is going to be incorporated
        ki = xmlsig.template.ensure_key_info(signature, name=key_info_id)
        data = xmlsig.template.add_x509_data(ki)
        xmlsig.template.x509_data_add_certificate(data)
        serial = xmlsig.template.x509_data_add_issuer_serial(data)
        xmlsig.template.x509_issuer_serial_add_issuer_name(serial)
        xmlsig.template.x509_issuer_serial_add_serial_number(serial)
        xmlsig.template.add_key_value(ki)
        qualifying = template.create_qualifying_properties(
            signature, name=utils.get_unique_id(), etsi='xades'
        )
        # Add additional data por the signature
        props = template.create_signed_properties(
            qualifying, name=signature_id
        )
        # Additional data for signature
        if signer_role:
            if signer_role not in SIGNER_ROLE:
                raise FacturaeSignError(
                    f'Signer role \'{signer_role}\' is invalid. '
                    f'Has to be one of the following roles: {SIGNER_ROLE}'
                )
            template.add_claimed_role(props, signer_role)
        if signature_production_place:
            template.add_production_place(props, **signature_production_place)
        # Add policy info
        policy = GenericPolicyId(
            SIGN_POLICY,
            "Política de firma electrónica para facturación "
            "electrónica con formato Facturae",
            xmlsig.constants.TransformSha1,
        )
        # Append the signature to the parsed document
        parsed_file.append(signature)

        # Add policy to ctx for signig in the next step
        ctx = XAdESContext(policy)
        # Load the certificate and private key to the ctx
        # and perform the signing
        with open(public_cert, "rb") as public_cert_file:
            certificate = x509.load_pem_x509_certificate(
                public_cert_file.read()
            )
        ctx.x509 = certificate
        ctx.public_key = certificate.public_key()
        with open(private_key, "rb") as private_key_file:
            ctx.private_key = serialization.load_pem_private_key(
                private_key_file.read(), password=None
            )
        ctx.sign(signature)
        string_signed_root = etree.tostring(parsed_file)
        return string_signed_root

    @classmethod
    def sign_pkcs12(cls, xml, certificate, password):
        """Sign pkcs12 certificate"""
        pkcs12_key, pkcs12_cert = cls.extract_from_pkcs12(
            pk=certificate, passwd=password
        )
        try:
            string_signed_root = FacturaeUtils.sign_xmldsig(
                xml, pkcs12_cert, pkcs12_key
            )
        except Exception as e:
            _logger.error(f'Error occurred while trying to sign facturae '
                          f'xml with provided certificate: {e}')
            raise FacturaeSignError('Fail to sign facturae')
        return string_signed_root

    @classmethod
    def sign_x509(cls, xml, certificate, private_key):
        """
        Sign X509 certificate
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
            _logger.error(f'Error occurred while trying to load key and '
                          f'certificate from a X509 certificate: {e}')
            raise FacturaeSignError('Fail to load key and certificate')
        string_signed_root = FacturaeUtils.sign_xmldsig(xml, cert, priv_key)
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
            _logger.error(f'Error occurred while trying to load key and '
                          f'certificate from a PKCS12 certificate: {e}')
            raise FacturaeSignError('Fail to load key and certificate')
