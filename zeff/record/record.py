"""Zeff record."""
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["Record"]

import dataclasses

from .structured_data import StructuredData
from .unstructured_data import UnstructuredData


@dataclasses.dataclass()
class Record:
    """This represents a single record in Zeff.

    :property name: The unique name for the record.
    """

    name: str
    structured_data: StructuredData = dataclasses.field(init=False)
    unstructured_data: UnstructuredData = dataclasses.field(init=False)

    def __post_init__(self):
        """Add missing required items."""
        self.structured_data = StructuredData()
        self.unstructured_data = UnstructuredData()

    def validate(self):
        """Validate to ensure that it will be accepted on upload.

        :exception TypeError: If a property in a record is an incorrect type.

        :exception ValueError: If a property in a record is not within
            acceptable range (e.g. expects a continuous value such as
            integer but gets a descrete value such as a string).
        """
        # pylint: disable=no-member
        if self.structured_data is None:
            raise ValueError("structured_data must be set")
        self.structured_data.validate()
        if self.unstructured_data is None:
            raise ValueError("unstructured_data must be set")
        self.unstructured_data.validate()
