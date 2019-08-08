"""Zeff test suite."""

import pytest
import enum

from zeff.record import StructuredData


def test_build():
    """Test building a StructuredData."""
    sd0 = StructuredData(
        "TestName", 1.1, StructuredData.DataType.CONTINUOUS, StructuredData.Target.YES
    )
    assert sd0.record is None
    sd0.validate()

    sd1 = StructuredData(
        "TestName",
        "TestValue",
        StructuredData.DataType.CATEGORY,
        StructuredData.Target.YES,
    )
    assert sd1.record is None
    sd1.validate()


def test_invalid_strutureddatatype():
    """Attempt to add an invalid data type to a StructuredData."""
    with pytest.raises(TypeError):
        sd = StructuredData(
            "TestName", "TestValue", StructuredData.DataType.CONTINUOUS, "TestTarget"
        )
        sd.validate()
    with pytest.raises(TypeError):
        sd = StructuredData(
            "TestName", "TestValue", "TestDataType", StructuredData.Target.YES
        )
        sd.validate()


def test_invalid_structuredtarget():
    """TBW"""
    with pytest.raises(ValueError):
        sd = StructuredData(
            "TestName",
            "abc",
            StructuredData.DataType.CONTINUOUS,
            StructuredData.Target.NO,
        )
        sd.validate()


def test_unknown_structureddatatype():
    """Check to make sure a test will fail if a new data type is added."""

    class TestDataType(enum.Enum):
        CONTINUOUS = enum.auto()
        CATEGORY = enum.auto()
        SPAM = enum.auto()

    old = StructuredData.DataType
    with pytest.raises(ValueError):
        StructuredData.DataType = TestDataType
        sd = StructuredData(
            "TestName", "abc", StructuredData.DataType.SPAM, StructuredData.Target.NO
        )
        sd.validate()
    StructuredData.DataType = old
