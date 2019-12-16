"""Zeff record generate, build, validate, and upload pipeline."""
__docformat__ = "reStructuredText en"
__all__ = ["Counter", "record_builder_generator", "validation_generator"]

import logging

LOGGER_GENERATOR = logging.getLogger("zeffclient.record.generator")
LOGGER_BUILDER = logging.getLogger("zeffclient.record.builder")
LOGGER_VALIDATOR = logging.getLogger("zeffclient.record.validator")
LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


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


def record_builder_generator(model, upstream, builder):
    """Build and yield records from a configuration upstream.

    :param model: If true then all records will be allowed, but if
        false then records not used for training will be filtered.

    :param upstream: The object that will generate configuration
       strings used to build a record.

    :param builder: Callable object that will take a configuration
       string and return a record.
    """
    for config in upstream:
        record = builder(model, config)
        if record is None:
            continue
        yield record


def validation_generator(upstream, validator):
    """Validate records from generator and yield valid records.

    :param upstream: A generator that will yield record objects that
        may be validated.

    :param validator: A callable object that will take a
        single parameter that is the record to be validated.

    :return: Records that only have validation warnings.
    """
    for record in upstream:
        try:
            validator(record)
            yield record
        except TypeError as err:
            LOGGER_VALIDATOR.error(err)
        except ValueError as err:
            LOGGER_VALIDATOR.error(err)
