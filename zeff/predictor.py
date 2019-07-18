"""Zeff build, and upload record for Zeff Cloud to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["Predictor"]

import logging

LOGGER_SUBMITTER = logging.getLogger("zeffclient.record.uploader")


class Predictor:
    """Upload a record to make prediction and report results."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """TBW."""

    def __call__(self, record):
        """TBW."""
        print("Predictor not built")
