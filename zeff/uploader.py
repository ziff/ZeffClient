"""Zeff upload records to Zeff Cloud dataset."""
__docformat__ = "reStructuredText en"
__all__ = ["Uploader"]

import logging

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Uploader:
    """Generator that will yield successfully uploaded records.

    :param upstream: Generator of records to be uploaded.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, upstream):
        """TBW."""
        self.upstream = upstream

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        record = next(self.upstream)
        print("Uploader not built", record)
        return record
