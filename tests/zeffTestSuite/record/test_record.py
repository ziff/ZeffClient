"""Zeff test suite."""

import pytest

from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    Target,
    DataType,
    FileType,
)
from zeff.validator import RecordValidator


def test_build():
    """Test building a record.

    This will check to make sure that all dataclasses
    associated with a Record can be built and added to
    appropriate containers.
    """
    r = Record("Test")

    ## StructuredData
    sd = StructuredData("TestName", 1.1, DataType.CONTINUOUS, Target.YES)
    assert sd.record is None
    sd.record = r
    assert sd in list(r.structured_data)
    assert len(list(r.structured_data)) == 1

    ## UnstructuredData
    ud = UnstructuredData("http://example.com", FileType.TEXT)
    assert ud.record is None
    ud.record = r
    assert ud in list(r.unstructured_data)
    assert len(list(r.unstructured_data)) == 1

    ## Validate
    rv = RecordValidator(True)
    rv(r)
