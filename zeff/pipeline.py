"""Zeff record generate, build, validate, and upload pipeline."""
__docformat__ = "reStructuredText en"
__all__ = ["Counter", "record_builder_generator", "validation_generator"]

import logging

LOGGER_BUILDER = logging.getLogger("zeffclient.record.builder")
LOGGER_GENERATOR = logging.getLogger("zeffclient.record.generator")
LOGGER_VALIDATOR = logging.getLogger("zeffclient.record.validator")
LOGGER_SUBMITTER = logging.getLogger("zeffclient.record.submitter")


class Counter:
    """Generator that will count objects that pass through it."""

    def __init__(self, upstream):
        """Create a new counter on ``upstream``."""
        self.count = 0
        self.upstream = iter(upstream)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        ret = next(self.upstream)
        self.count = self.count + 1
        return ret


def record_builder_generator(upstream, builder):
    """Build and yield records from a configuration upstream.

    :param upstream: The object that will generate configuration
       strings used to build a record.

    :param builder: Callable object that will take a configuration
       string and return a record.
    """
    for config in upstream:
        record = builder(config)
        yield record


def validation_generator(upstream):
    """Validate records from generator and yield valid records.

    :param upstream: A generator that will yield record objects that
        may be validated.

    :return: Records that only have validation warnings.
    """
    for record in upstream:
        try:
            LOGGER_VALIDATOR.info("Begin validation record %s", record.name)
            record.validate()
            LOGGER_VALIDATOR.info("End validation record %s", record.name)
            yield record
        except TypeError as err:
            LOGGER_VALIDATOR.exception(err, record=record)
            continue
        except ValueError as err:
            LOGGER_VALIDATOR.exception(err, record=record)
            continue
