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

    ## StructuredData
    sd = r.structured_data
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
    ud = r.unstructured_data
    udi = UnstructuredDataItem("http://example.com", UnstructuredDataItem.FileType.TEXT)
    assert udi.unstructured_data is None
    udi.unstructured_data = ud
    assert udi in list(ud.unstructured_data_items)
    assert len(list(ud.unstructured_data_items)) == 1

    ## Validate

    r.validate()
