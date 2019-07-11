"""Zeff record."""
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["Record"]

import dataclasses


@dataclasses.dataclass()
class Record:
    """This represents a single record in Zeff.

    :property name: The unique name for the record.
    """

    name: str

    def validate(self):
        """Validate to ensure that it will be accepted on upload.

        :exception TypeError: If a property in a record is an incorrect type.

        :exception ValueError: If a property in a record is not within
            acceptable range (e.g. expects a continuous value such as
            integer but gets a descrete value such as a string).
        """
        # pylint: disable=no-member
        for data in self.structured_data:
            data.validate()
        for data in self.unstructured_data:
            data.validate()
