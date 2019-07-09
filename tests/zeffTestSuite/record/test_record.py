"""Zeff test suite."""

import pytest

from zeff.record import (
    Record,
    StructuredData,
    StructuredDataItem,
    UnstructuredData,
    UnstructuredDataItem,
)


def test_build():
    """Test building a record.

    This will check to make sure that all dataclasses
    associated with a Record can be built and added to
    appropriate containers.
    """
    r = Record("Test")
    assert len(list(r.structured_data)) == 0
    assert len(list(r.unstructured_data)) == 0

    ## StructuredData

    sd = StructuredData()
    assert sd.record is None
    sd.record = r
    assert sd.record == r
    assert sd in list(r.structured_data)
    assert len(list(r.structured_data)) == 1

    sdi = StructuredDataItem(
        "TestName",
        1.1,
        StructuredDataItem.DataType.CONTINUOUS,
        StructuredDataItem.Target.YES,
    )
    assert sdi.structured_data is None
    sdi.structured_data = sd
    assert sdi in list(sd.structured_data_items)
    assert len(list(sd.structured_data_items)) == 1

    ## UnstructuredData

    ud = UnstructuredData()
    assert ud.record is None
    ud.record = r
    assert ud.record == r
    assert ud in list(r.unstructured_data)
    assert len(list(r.unstructured_data)) == 1

    udi = UnstructuredDataItem("http://example.com", "text/plain")
    assert udi.unstructured_data is None
    udi.unstructured_data = ud
    assert udi in list(ud.unstructured_data_items)
    assert len(list(ud.unstructured_data_items)) == 1

    ## Validate

    r.validate()


def test_invalid_aggregation():
    """Test that invalid associations are prohibited.

    This mainly tests that ``aggregation`` is working correctly.
    """
    r0 = Record("Test0")
    r1 = Record("Test1")
    sd = StructuredData()

    with pytest.raises(ValueError):
        sd.record = None

    with pytest.raises(TypeError):
        sd.record = "SPAM"

    sd.record = r0
    with pytest.raises(ValueError):
        sd.record = r1

    del sd.record
