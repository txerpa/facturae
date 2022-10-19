import os
from contextlib import nullcontext as does_not_raise

import pytest

from facturae.constants import XSD_MAP_VERSIONS, XSL_MAP_VERSIONS
from facturae.exceptions import VersionNotExpected
from facturae.utils import FacturaeUtils


def get_file_data_from_version_path(version):
    file_version = version.replace(".", "_")
    path = f"fixtures/xml_v{file_version}.xml"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
    with open(path, "rb") as f:
        data = f.read()
    return data


@pytest.mark.parametrize("version", dict(XSL_MAP_VERSIONS).keys())
def test_check_xsl_versions(version):
    xml_data = get_file_data_from_version_path(version)
    html = FacturaeUtils.to_html(xml_data, version)
    assert html.startswith(b"<html")


@pytest.mark.parametrize("version", dict(XSD_MAP_VERSIONS).keys())
def test_check_xsd_versions(version):
    xml_data = get_file_data_from_version_path(version)
    FacturaeUtils.validate_xml(xml_data, version)
    assert True


test_values = [
    ("fail", pytest.raises(VersionNotExpected)),
]
test_values.extend(map(lambda v: [v, does_not_raise()], dict(XSD_MAP_VERSIONS).keys()))


@pytest.mark.parametrize("version,expectation", test_values)
def test_check_xsd_versions_fail(version, expectation):
    with expectation:
        FacturaeUtils.get_xsd_file(version)
