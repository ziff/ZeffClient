"""Zeff unstructured data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["UnstructuredData", "UnstructuredDataItem"]

import dataclasses
from typing import Optional
import re

from .aggregator import aggregation
from .record import Record


@aggregation(Record)
@dataclasses.dataclass(unsafe_hash=True)
class UnstructuredData:
    """This represents a set of unstructured data items."""

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""
        # pylint: disable=no-member
        for item in self.unstructured_data_items:
            item.validate()


@aggregation(UnstructuredData, contained_prop_name="unstructured_data_items")
@dataclasses.dataclass(eq=True, frozen=True)
class UnstructuredDataItem:
    """Single item in UnstruturedData.

    An unstructured data time is a URI to ``data`` that has an
    associated media type and may be grouped with other similar
    data.

    :property data: URI to the raw data.

    :property media_type: An RFC 2046 media type of the data.

    :property group_by: Name of a groupd this item should be
        associated with.
    """

    data: str
    media_type: str
    group_by: Optional[str] = None

    re_mediatype = re.compile(
        r"""(?ax)^
            (?P<type>.[a-zA-Z0-9][a-zA-Z0-9!#$&\-^_]{0,126})
            /
            (?P<subtype>.[a-zA-Z0-9][a-zA-Z0-9!#$&\-^_]{0,126})
            (?P<parameters>(;
                [!#$%&'*+\-.0-9A-Z^_`a-z|~]+
                =
                (([!#$%&'*+\-.0-9A-Z^_`a-z|~]+)|("[^"]+"))
            )*)
            $"""
    )

    def validate(self):
        """Validate to ensure that it will be accepted on upload."""

        # RFC6838 Media Type Specifications and Registration Procedures
        if UnstructuredDataItem.re_mediatype.match(self.media_type) is None:
            raise ValueError(f"Invalid media type `{self.media_type}`")
