"""Zeff test suite."""

import pytest
import enum

from zeff.record import StructuredData, StructuredDataItem


def test_build():
    """Test building a StructuredData."""
    sd = StructuredData()
    assert sd.record is None

    sdi0 = StructuredDataItem(
        "TestName",
        1.1,
        StructuredDataItem.DataType.CONTINUOUS,
        StructuredDataItem.Target.YES,
    )
    assert sdi0.structured_data is None
    sdi0.structured_data = sd
    assert sdi0 in list(sd.structured_data_items)
    assert len(list(sd.structured_data_items)) == 1

    sdi1 = StructuredDataItem(
        "TestName",
        "TestValue",
        StructuredDataItem.DataType.CATEGORY,
        StructuredDataItem.Target.YES,
    )
    assert sdi1.structured_data is None
    sdi1.structured_data = sd
    assert sdi1 in list(sd.structured_data_items)
    assert len(list(sd.structured_data_items)) == 2

    sd.validate()


def test_invalid_strutureddatatype():
    """Attempt to add an invalid data type to a StructuredDataItem."""
    with pytest.raises(TypeError):
        sdi = StructuredDataItem(
            "TestName",
            "TestValue",
            StructuredDataItem.DataType.CONTINUOUS,
            "TestTarget",
        )
        sdi.validate()
    with pytest.raises(TypeError):
        sdi = StructuredDataItem(
            "TestName", "TestValue", "TestDataType", StructuredDataItem.Target.YES
        )
        sdi.validate()


def test_invalid_structuredtarget():
    """TBW"""
    with pytest.raises(ValueError):
        sdi = StructuredDataItem(
            "TestName",
            "abc",
            StructuredDataItem.DataType.CONTINUOUS,
            StructuredDataItem.Target.NO,
        )
        sdi.validate()


def test_unknown_structureddatatype():
    """Check to make sure a test will fail if a new data type is added."""

    class TestDataType(enum.Enum):
        CONTINUOUS = enum.auto()
        CATEGORY = enum.auto()
        SPAM = enum.auto()

    old = StructuredDataItem.DataType
    with pytest.raises(ValueError):
        StructuredDataItem.DataType = TestDataType
        sdi = StructuredDataItem(
            "TestName",
            "abc",
            StructuredDataItem.DataType.SPAM,
            StructuredDataItem.Target.NO,
        )
        sdi.validate()
    StructuredDataItem.DataType = old
