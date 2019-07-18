"""Zeff record generate, build, validate, and upload pipeline."""
__docformat__ = "reStructuredText en"
__all__ = ["pipeline"]

import logging

LOGGER_BUILDER = logging.getLogger("zeffclient.record.builder")
LOGGER_GENERATOR = logging.getLogger("zeffclient.record.generator")
LOGGER_VALIDATOR = logging.getLogger("zeffclient.record.validator")
LOGGER_SUBMITTER = logging.getLogger("zeffclient.record.submitter")


def pipeline(generator, builder, validator, uploader):
    """Pipeline to generate, build, validate, and upload records.

    :param generator: The object that will generate configuration strings.

    :param builder: A callable object that will take a configuration string
        and return a record.

    :param validator: A callable object that will take a record to be
        validated.

    :param uploader: A callable object that will take a record to be
        uploaded.

    :return: True if all records were built, validated, and uploaded.
        False if any record could not be built, failed validation,
        or did not upload.
    """
    ret = True

    for config in generator:
        record = builder(config)
        try:
            validator(record)
        except TypeError as err:
            ret = False
            LOGGER_VALIDATOR.exception(err)
            continue
        except ValueError as err:
            ret = False
            LOGGER_VALIDATOR.exception(err)
            continue
        uploader(record)
    return ret
