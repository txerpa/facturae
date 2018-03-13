# -*- coding: utf-8 -*-
__author__ = 'XaviTorello'

import sys
sys.path.insert(0, '.')

from facturae import facturae
import specs as test_data

import logging
#logging.basicConfig(level=logging.DEBUG)

with description('Invoice'):
    with before.each:
        self.invoice = facturae.FacturaeRoot()

        header = None
        parties = None
        invoices = None

        self.invoice.feed({
            'fileheader': header,
            'parties': parties,
            'invoices': invoices,
        })

        assert test_data.CERTIFICATE and test_data.CERTIFICATE_PASSWD and test_data.CERTIFICATE_PUBLIC
        self.certificate = open(test_data.CERTIFICATE).read()
        self.certificate_public = open(test_data.CERTIFICATE_PUBLIC).read().replace("-----BEGIN CERTIFICATE-----","").replace("-----END CERTIFICATE-----","").replace("\n","")
        self.password = test_data.CERTIFICATE_PASSWD


    with context('sign'):
        with it('must work as expected'):
            signed = self.invoice.sign(self.certificate, self.password)

            # [!] Public component of provided cert must be inside the signed XML
            assert self.certificate_public in signed, "Expected current certificate '{}' must be inside the signed Invoice".format(test_data.CERTIFICATE_PUBLIC)
