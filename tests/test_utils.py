import pytest

from facturae.constants import XSD_MAP_VERSIONS, XSL_MAP_VERSIONS
from facturae.exceptions import VersionNotExpected
from facturae.utils import FacturaeUtils
from tests.fixtures import XML_FILES, XML_V3_2_2


@pytest.mark.parametrize("version,_", XSL_MAP_VERSIONS)
def test_check_xsl_versions(version, _):
    html = FacturaeUtils.to_html(XML_FILES[f"v{version}"], version)
    assert html.startswith(b"<html")


@pytest.mark.parametrize("version,_", XSD_MAP_VERSIONS)
def test_check_xsd_versions(version, _):
    FacturaeUtils.validate_xml(XML_FILES[f"v{version}"], version)
    assert True


def test_check_xsd_versions_fail():
    with pytest.raises(VersionNotExpected):
        FacturaeUtils.validate_xml(XML_V3_2_2, "---")
