"""Zeff record."""
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["Record"]

import dataclasses
import typing
from .structureddata import StructuredData
from .unstructureddata import UnstructuredData


@dataclasses.dataclass()
class Record:
    """This represents a single record in Zeff.

    :property name: The unique name for the record.

    :property structured_data: List of ``StructuredData`` objects that
        belong to this record. This list should not be modified directly;
        setting ``StructuredData.record`` property will add the object
        to the list.

    :property unstructured_data: List of ``UnstructuredData`` objects that
        belong to this record. This list should not be modified directly;
        setting ``UnstructuredData.record`` property will add the object
        to the list.
    """

    name: str
    structured_data: typing.List[StructuredData] = dataclasses.field(
        default_factory=list
    )
    unstructured_data: typing.List[UnstructuredData] = dataclasses.field(
        default_factory=list
    )

    def __str__(self):
        """`__str__<https://docs.python.org/3/reference/datamodel.html#object.__str__>`_."""
        return self.name
