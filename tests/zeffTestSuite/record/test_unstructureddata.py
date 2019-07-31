"""Zeff test suite."""

import pytest
import enum

from zeff.record import UnstructuredData, UnstructuredDataItem


def test_valid_http():
    """Test building a UnstructuredData."""
    ud = UnstructuredData()
    udi = UnstructuredDataItem("http://example.com", UnstructuredDataItem.FileType.TEXT)
    assert udi.unstructured_data is None
    udi.unstructured_data = ud
    assert udi in list(ud.unstructured_data_items)
    assert len(list(ud.unstructured_data_items)) == 1

    ud.validate()
    assert udi.accessible == "OK"


def test_valid_file():
    """Test building a UnstructuredData with file."""
    ud = UnstructuredData()
    udi = UnstructuredDataItem(f"file://{__file__}", UnstructuredDataItem.FileType.TEXT)
    assert udi.unstructured_data is None
    udi.unstructured_data = ud
    assert udi in list(ud.unstructured_data_items)
    assert len(list(ud.unstructured_data_items)) == 1

    ud.validate()
    assert udi.accessible == "OK"


def test_missing_file():
    """Test building a UnstructuredData with missing file."""
    udi = UnstructuredDataItem("file:///spam", UnstructuredDataItem.FileType.TEXT)
    udi.validate()
    assert udi.accessible == "file missing"


def test_invalid_file():
    """Test building a UnstructuredData with invalid file."""
    udi = UnstructuredDataItem("file:///var", UnstructuredDataItem.FileType.TEXT)
    udi.validate()
    assert udi.accessible == "not a file"


def test_permissions_file():
    """Test building a UnstructuredData with no read permissions."""
    udi = UnstructuredDataItem(
        "file:///etc/sudoers", UnstructuredDataItem.FileType.TEXT
    )
    udi.validate()
    assert udi.accessible != "OK"


def test_invalid_url_scheme():
    """Test building a UnstructuredData with invalid URL scheme."""
    udi = UnstructuredDataItem(
        "spam://example.com/", UnstructuredDataItem.FileType.TEXT
    )
    udi.validate()
    assert udi.accessible.lower().startswith("unknown url scheme")


def test_invalid_mediatype():
    """Attempt to set an invalid media type."""
    with pytest.raises(TypeError):
        udi = UnstructuredDataItem("http://example.com", "InvalidMedia")
        udi.validate()
