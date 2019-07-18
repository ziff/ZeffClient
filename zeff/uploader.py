"""Zeff upload records to Zeff Cloud dataset."""
__docformat__ = "reStructuredText en"
__all__ = ["Uploader"]

import logging

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Uploader:
    """Class that handles uploading of records to Zeff Cloud."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """TBW."""

    def __call__(self, record):
        """TBW."""
        print("Uploader not built", record)
