"""Zeff test suite."""

import pytest
import enum

from zeff.record import StructuredData, Target, DataType
from zeff.validator import RecordValidator


def test_build():
    """Test building a StructuredData."""
    validator = RecordValidator(True)

    sd0 = StructuredData("TestName", 1.1, DataType.CONTINUOUS, Target.YES)
    assert sd0.record is None
    validator.validate_structured_data(sd0)

    sd1 = StructuredData("TestName", "TestValue", DataType.CATEGORY, Target.YES)
    assert sd1.record is None
    validator.validate_structured_data(sd1)


def test_invalid_strutureddatatype():
    """Attempt to add an invalid data type to a StructuredData."""
    validator = RecordValidator(True)

    with pytest.raises(TypeError):
        sd = StructuredData("TestName", "TestValue", DataType.CONTINUOUS, "TestTarget")
        validator.validate_structured_data(sd)
    with pytest.raises(TypeError):
        sd = StructuredData("TestName", "TestValue", "TestDataType", Target.YES)
        validator.validate_structured_data(sd)


def test_invalid_structuredtarget():
    """TBW"""
    validator = RecordValidator(True)
    with pytest.raises(ValueError):
        sd = StructuredData("TestName", "abc", DataType.CONTINUOUS, Target.NO)
        validator.validate_structured_data(sd)


@pytest.mark.skip()
def test_unknown_structureddatatype():
    """Check to make sure a test will fail if a new data type is added."""
    global DataType

    class TestDataType(enum.Enum):
        CONTINUOUS = enum.auto()
        CATEGORY = enum.auto()
        SPAM = enum.auto()

    validator = RecordValidator(True)
    old = DataType
    with pytest.raises(ValueError):
        DataType = TestDataType
        sd = StructuredData("TestName", "abc", DataType.SPAM, Target.NO)
        validator.validate_structured_data(sd)
    DataType = old
