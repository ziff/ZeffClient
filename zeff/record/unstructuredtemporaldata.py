"""Zeff unstructured temporal data."""
# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
__docformat__ = "reStructuredText en"
__all__ = ["UnstructuredTemporalData"]

import dataclasses
import typing
import datetime
from .file import FileContext
from .unstructureddata import UnstructuredData


@dataclasses.dataclass
class UnstructuredTemporalData(UnstructuredData):
    """Single item of unstructured temporal data in a record.

    :property temporal_window: Size of window to analyze. This
        is a required property and if missing the data will
        fail in validation.

    :property start_crop_time: Time location from begining of file
        that will mark the start of the interval. Content before start
        point will not be used to train the Ai.

    :property end_crop_time: Time location from begining of file
        that will mark the end of the interval. Content after end
        point will not be used to train the Ai.

    :property file_context:
    """

    temporal_window: typing.Optional[datetime.time] = None
    start_crop_time: typing.Optional[datetime.time] = None
    end_crop_time: typing.Optional[datetime.time] = None
    file_contexts: typing.List[FileContext] = dataclasses.field(default_factory=list)
