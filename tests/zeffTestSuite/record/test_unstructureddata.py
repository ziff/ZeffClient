"""Zeff test suite."""

import pytest
import enum

from zeff.record import UnstructuredData


def test_valid_http():
    """Test building a UnstructuredData."""
    ud = UnstructuredData("http://example.com", UnstructuredData.FileType.TEXT)
    assert ud.record is None
    ud.validate()
    assert ud.accessible == "OK"


def test_valid_file():
    """Test building a UnstructuredData with file."""
    ud = UnstructuredData(f"file://{__file__}", UnstructuredData.FileType.TEXT)
    assert ud.record is None
    ud.validate()
    assert ud.accessible == "OK"


def test_missing_file():
    """Test building a UnstructuredData with missing file."""
    ud = UnstructuredData("file:///spam", UnstructuredData.FileType.TEXT)
    ud.validate()
    assert ud.accessible == "file missing"


def test_invalid_file():
    """Test building a UnstructuredData with invalid file."""
    ud = UnstructuredData("file:///var", UnstructuredData.FileType.TEXT)
    ud.validate()
    assert ud.accessible == "not a file"


def test_permissions_file():
    """Test building a UnstructuredData with no read permissions."""
    ud = UnstructuredData("file:///etc/sudoers", UnstructuredData.FileType.TEXT)
    ud.validate()
    assert ud.accessible != "OK"


def test_invalid_url_scheme():
    """Test building a UnstructuredData with invalid URL scheme."""
    ud = UnstructuredData("spam://example.com/", UnstructuredData.FileType.TEXT)
    ud.validate()
    assert ud.accessible.lower().startswith("unknown url scheme")


def test_invalid_mediatype():
    """Attempt to set an invalid media type."""
    with pytest.raises(TypeError):
        ud = UnstructuredData("http://example.com", "InvalidMedia")
        ud.validate()
