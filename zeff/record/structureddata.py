"""Zeff structured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["StructuredData"]

import dataclasses
from .symbolic import Target, DataType


@dataclasses.dataclass(eq=True)
class StructuredData:
    """Single item of structured data in a record.

    A structured data is a mapping of ``name`` to ``value`` with
    additional information about the ``value``.

    :property name: The unique key that identifies this data item.

    :property value: The value stored in this data item.

    :property target: How a data item is to be used in training or inference.
        This  property is ignored by temporal records (`TemporalRecord`),
        and will not be sent to the Cloud API.

    :property data_type: Is the data continuous or discrete.

    :property record: The record for this data item. Setting this
        property will add this item to ``Record.structured_data``
        list automatically.
    """

    name: str
    value: object
    data_type: DataType
    target: Target = Target.IGNORE

    __record: object = None

    @property
    def record(self):
        """Record that contains this structured data item."""
        return self.__record

    @record.setter
    def record(self, value):
        del self.record
        self.__record = value
        value.structured_data.append(self)

    @record.deleter
    def record(self):
        if self.__record:
            self.__record.structured_data.remove(self)
            self.__record = None
