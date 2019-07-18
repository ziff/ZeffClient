"""Zeff CLI utility record builders."""
__all__ = ["EchoRecordBuilder", "NameRecordBuilder"]

import logging
from zeff.record import Record

LOGGER = logging.getLogger("zeffclient.record.builder")


class EchoRecordBuilder:
    """Prints the config string to stdout and returns no record."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **argv):
        """TBW."""

    def __call__(self, config):
        """TBW."""
        LOGGER.info("Begin building ``Echo`` record from %s", config)
        print(f"Record Config: {config}")
        LOGGER.info("End building ``Echo`` record from %s", config)


class NameRecordBuilder:
    """Creates a record with config string as name."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **argv):
        """TBW."""

    def __call__(self, config):
        """TBW."""
        LOGGER.info("Begin building ``Name`` record from %s", config)
        ret = Record(name=config)
        LOGGER.info("End building ``Name`` record from %s", config)
        return ret
