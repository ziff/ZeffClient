"""Zeff unstructured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["UnstructuredData"]

import dataclasses
from typing import Optional
from .symbolic import FileType


@dataclasses.dataclass(eq=True)
class UnstructuredData:
    """Single item of unstructured data in a record.

    An unstructured data is a URI to ``data`` that has an
    associated file type and may be grouped with other similar
    data.

    :property data_uri: URI to the raw data.

    :property file_type: The file type of the data.

    :property group_by: Name of group this item should be
        associated with.

    :property upload: Indicates that the ``data`` should be uploaded
        to the Zeff API when this data item is uploaded (default is
        for the server to access the data directly using the URL in
        ``data``).

    :property accessible: Flag set during validation that the
        location given by ``data_uri`` is accessible.

    :property record: The record for this data item. Setting this
        property will add this item to ``Record.unstructured_data``
        list automatically.
    """

    data_uri: str
    file_type: FileType
    group_by: Optional[str] = None
    upload: bool = False
    accessible: str = dataclasses.field(
        default="", init=False, repr=False, compare=False
    )
    __record: object = None

    @property
    def record(self):
        """Record that contains this unstructured data item."""
        return self.__record

    @record.setter
    def record(self, value):
        del self.record
        self.__record = value
        value.unstructured_data.append(self)

    @record.deleter
    def record(self):
        if self.__record:
            self.__record.unstructured_data.remove(self)
            self.__record = None
