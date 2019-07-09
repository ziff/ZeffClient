"""Zeff test suite."""

import pytest
import enum

from zeff.record import UnstructuredData, UnstructuredDataItem


def test_build():
    """Test building a UnstructuredData."""
    ud = UnstructuredData()
    assert ud.record is None

    udi = UnstructuredDataItem("http://example.com", "text/plain")
    assert udi.unstructured_data is None
    udi.unstructured_data = ud
    assert udi in list(ud.unstructured_data_items)
    assert len(list(ud.unstructured_data_items)) == 1

    ud.validate()


def test_invalid_mediatype():
    """Attempt to set an invalid media type."""
    with pytest.raises(ValueError):
        udi = UnstructuredDataItem("http://example.com", "InvalidMedia")
        udi.validate()
    with pytest.raises(ValueError):
        udi = UnstructuredDataItem("http://example.com", "abc/xyz;")
        udi.validate()
    with pytest.raises(ValueError):
        udi = UnstructuredDataItem("http://example.com", "abc/xyz;param=")
        udi.validate()
