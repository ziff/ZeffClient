"""Zeff generate, build, and upload runner."""
__docformat__ = "reStructuredText en"
__all__ = ["runner"]

import logging

LOGGER_BUILDER = logging.getLogger("zeffclient.record_builder")
LOGGER_GENERATOR = logging.getLogger("zeffclient.record_generator")
LOGGER_VALIDATOR = logging.getLogger("zeffclient.record_validator")
LOGGER_SUBMITTER = logging.getLogger("zeffclient.record_submitter")


def runner(generator, builder, validator, uploader):
    """Process runner for record building, validating, and submitting.

    :param generator: The object that will generate configuration strings.

    :param builder: A callable object that will take a configuration string
        and return a record.

    :param validator: A callable object that will take a record to be
        validated.

    :param uploader: A callable object that will take a record to be
        uploaded.
    """

    for config in generator:
        record = builder(config)
        try:
            validator(record)
        except TypeError as err:
            LOGGER_VALIDATOR.exception(err)
            continue
        except ValueError as err:
            LOGGER_VALIDATOR.exception(err)
            continue
        uploader(record)
