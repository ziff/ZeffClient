"""Zeff record file reference."""
__docformat__ = "reStructuredText en"
__all__ = ["FileContext"]

import dataclasses
import typing
import datetime
from .symbolic import DataType


@dataclasses.dataclass(eq=True, frozen=True)
class FileContext:
    """Structured data associated with a time interval.

    .. caution:: Subcontext is only allowed to be used in a
        FileContext that is added directly to an unstructured
        temporal data object.
    """

    name: str
    value: object
    data_type: DataType
    start_time: datetime.time
    end_time: datetime.time
    subcontexts: typing.List["FileContext"] = dataclasses.field(default_factory=list)
