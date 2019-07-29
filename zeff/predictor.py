"""Zeff build, and upload record for Zeff Cloud to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["Predictor"]

import logging

LOGGER_SUBMITTER = logging.getLogger("zeffclient.record.uploader")


class Predictor:
    """Upload a record to make prediction and report results.

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
        print("Predictor not built", record)
        return record
