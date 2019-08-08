"""Zeff unstructured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["UnstructuredData"]

import dataclasses
import enum
from typing import Optional
import urllib.parse
import urllib.request
import pathlib

from .record import Record
from .aggregator import aggregation


@aggregation(Record, contained_prop_name="unstructured_data")
@dataclasses.dataclass(eq=True, frozen=True)
class UnstructuredData:
    """Single item of unstructured data in a record.

    An unstructured data is a URI to ``data`` that has an
    associated file type and may be grouped with other similar
    data.

    :property data: URI to the raw data.

    :property file_type: The file type of the data.

    :property group_by: Name of a groupd this item should be
        associated with.
    """

    class FileType(enum.Enum):
        """File type of a unstructured data item."""

        IMAGE = enum.auto()
        AUDIO = enum.auto()
        VIDEO = enum.auto()
        DOCUMENT = enum.auto()
        META = enum.auto()
        TEXT = enum.auto()

    data: str
    file_type: FileType
    group_by: Optional[str] = None
    accessible: str = dataclasses.field(
        default="", init=False, repr=False, compare=False
    )

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""

        if self.file_type not in UnstructuredData.FileType:
            raise TypeError(f"file_type `{self.file_type}` is not FileType")

        parts = urllib.parse.urlsplit(self.data)
        if parts[0] == "file":
            value = "OK"
            path = pathlib.Path(parts[2])
            if not path.exists():
                value = "file missing"
            elif not path.is_file():
                value = "not a file"
            else:
                try:
                    path.open("r").close()
                except OSError as err:
                    value = str(err)
        elif parts[0] in ["http", "https"]:
            url = "https://docs.python.org/3/library/urllib.request.html"
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req)
            value = resp.reason
        else:
            value = f"Unknown URL scheme {parts[0]}"
        object.__setattr__(self, "accessible", value)
