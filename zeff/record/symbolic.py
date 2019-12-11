"""Zeff record symbols."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["Target", "DataType", "FileType"]

import enum


class Target(enum.Enum):
    """How the data item is to be used in training or inference.

    - YES
        This is a desired outcome to be predicted.

    - NO
        This is an input to consume for predictions.

    - IGNORE
        Do not use in training or predition but may show in reporting
    """

    YES = enum.auto()
    NO = enum.auto()
    IGNORE = enum.auto()


class DataType(enum.Enum):
    """Data type of a structured data item.

    - CONTINUOUS
        Continuous data type such as integer or floating point.

    - CATEGORY
        Discrete data type such as a string.
    """

    CONTINUOUS = enum.auto()
    CATEGORY = enum.auto()


class FileType(enum.Enum):
    """File type of a unstructured data item."""

    IMAGE = enum.auto()
    AUDIO = enum.auto()
    VIDEO = enum.auto()
    DOCUMENT = enum.auto()
    META = enum.auto()
    TEXT = enum.auto()
