import pytest

from facturae.constants import XSD_MAP_VERSIONS, XSL_MAP_VERSIONS
from facturae.utils import FacturaeUtils
from tests.fixtures import XML_FILES


@pytest.mark.parametrize("version,_", XSL_MAP_VERSIONS)
def test_check_xsl_versions(version, _):
    html = FacturaeUtils.to_html(XML_FILES[f"v{version}"], version)
    assert html.startswith(b"<html")


@pytest.mark.parametrize("version,_", XSD_MAP_VERSIONS)
def test_check_xsd_versions(version, _):
    FacturaeUtils.validate_xml(XML_FILES[f"v{version}"], version)
    assert True
