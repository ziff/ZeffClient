"""Zeff structured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["StructuredData"]

import dataclasses
import enum

from .record import Record
from .aggregator import aggregation


@aggregation(Record, contained_prop_name="structured_data")
@dataclasses.dataclass(eq=True, frozen=True)
class StructuredData:
    """Single item of structured data in a record.

    A structured data is a mapping of ``name`` to ``value`` with
    additional information about the ``value``.

    :property name: The unique key that identifies this data item.

    :property value: The value stored in this data item.

    :property target: How a data item is to be used in training or inference.

    :property data_type: Is the data continuous or discrete.
    """

    class Target(enum.Enum):
        """How the data item is to be used in training or inference.

        - YES is a desired outcome to be predicted
        - NO is an input to consume for prediction
        - IGNORE do not use in training or predition but may show in reporting
        """

        YES = enum.auto()
        """Desired outcome to be predicted."""

        NO = enum.auto()
        """Input to consume for prediction."""

        IGNORE = enum.auto()
        """Do not use in training for prediction but may show in reporting."""

    class DataType(enum.Enum):
        """Data type of a structured data item."""

        CONTINUOUS = enum.auto()
        """Continuous data type such as integer or floating point."""

        CATEGORY = enum.auto()
        """Discrete data type."""

    name: str
    value: object
    data_type: DataType
    target: Target = Target.NO

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        if self.target not in StructuredData.Target:
            raise TypeError(
                f"StructuredData.target `{self.target}` is not a StructuredData.Target"
            )
        if self.data_type not in StructuredData.DataType:
            raise TypeError(f"data_type `{self.data_type}` is not DataType")
        if self.data_type == StructuredData.DataType.CONTINUOUS:
            if not isinstance(self.value, (int, float)):
                raise ValueError(
                    f"StructuredData.value `{self.value}` is not continuous"
                )
        elif self.data_type == StructuredData.DataType.CATEGORY:
            pass
        else:
            raise ValueError(f"Unknown StructuredData.data_type `{self.data_type}`")
