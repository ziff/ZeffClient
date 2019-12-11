"""Zeff test suite."""

import pytest
import enum

from zeff.record import UnstructuredData, FileType
from zeff.validator import RecordValidator


def test_valid_http():
    """Test building a UnstructuredData."""
    validator = RecordValidator(True)
    ud = UnstructuredData("http://example.com", FileType.TEXT)
    assert ud.record is None
    validator.validate_unstructured_data(ud)
    assert ud.accessible == "OK"


def test_valid_file():
    """Test building a UnstructuredData with file."""
    validator = RecordValidator(True)
    ud = UnstructuredData(f"file://{__file__}", FileType.TEXT)
    assert ud.record is None
    validator.validate_unstructured_data(ud)
    assert ud.accessible == "OK"


def test_missing_file():
    """Test building a UnstructuredData with missing file."""
    validator = RecordValidator(True)
    ud = UnstructuredData("file:///spam", FileType.TEXT)
    validator.validate_unstructured_data(ud)
    assert ud.accessible == "file missing"


def test_invalid_file():
    """Test building a UnstructuredData with invalid file."""
    validator = RecordValidator(True)
    ud = UnstructuredData("file:///var", FileType.TEXT)
    validator.validate_unstructured_data(ud)
    assert ud.accessible == "not a file"


def test_permissions_file():
    """Test building a UnstructuredData with no read permissions."""
    validator = RecordValidator(True)
    ud = UnstructuredData("file:///etc/sudoers", FileType.TEXT)
    validator.validate_unstructured_data(ud)
    assert ud.accessible != "OK"


def test_invalid_url_scheme():
    """Test building a UnstructuredData with invalid URL scheme."""
    validator = RecordValidator(True)
    ud = UnstructuredData("spam://example.com/", FileType.TEXT)
    validator.validate_unstructured_data(ud)
    assert ud.accessible.lower().startswith("unknown url scheme")


def test_invalid_mediatype():
    """Attempt to set an invalid media type."""
    validator = RecordValidator(True)
    with pytest.raises(TypeError):
        ud = UnstructuredData("http://example.com", "InvalidMedia")
        validator.validate_unstructured_data(ud)
