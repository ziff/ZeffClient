"""Zeff Validator."""
__docformat__ = "reStructuredText en"
__all__ = ["RecordValidator"]


import logging
import typing
import urllib.parse
import pathlib
from ..record import (
    Record,
    StructuredData,
    UnstructuredData,
    Target,
    DataType,
    FileType,
)
from ..pipeline import LOGGER_VALIDATOR


class RecordValidator:
    """Zeff Record Validator abstract base class.

    This validator will check that required items are in a generic
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """

    def __init__(self, model: bool, logger: logging.Logger = LOGGER_VALIDATOR):
        """Initialize a new record validator.

        :param model: Will this record be added to a dataset model or to
            a dataset. A dataset is used to train and a model is used
            to make inference.

        :param logger: A ``logging.Logger`` instance to assign to this
            validator. The default is ``zeffclient.record.validator``.
        """
        self.__model = model
        self.__logger = logger

    @property
    def model(self) -> bool:
        """If true this validator is for dataset model records."""
        return self.__model

    @property
    def logger(self) -> logging.Logger:
        """Logger assigned to this validator."""
        return self.__logger

    def __call__(self, record: Record):
        """Validate an individual record.

        This will return without exception if the record is valid,
        otherwise an exception will be thrown, and information will
        be placed on the logger, assigned to this validator,
        describing invalid data.

        .. CAUTION::
            Subclasses should not override this method; ``validate_yyz``
            method should be overriden instead.

        :exception TypeError: If a property in a record is an incorrect type.

        :exception ValueError: If a property in a record is not within
            acceptable range (e.g. expects a continuous value such as
            integer but gets a descrete value such as a string).
        """
        self.logger.info("Begin validating record %s", record.name)
        self.reset()
        try:
            self.validate_properties(record)
            self.validate_structured_data_aggregation(
                (d.name for d in record.structured_data)
            )
            for sdata in record.structured_data:
                self.validate_structured_data(sdata)
            if len(record.unstructured_data) < 1:
                raise ValueError(
                    "Record must have at least one UnstructuredData object."
                )
            for udata in record.unstructured_data:
                self.validate_unstructured_data(udata)
            self.validate_record(record)
        except TypeError as err:
            raise TypeError(f"Record {record.name}: {err}")
        except ValueError as err:
            raise ValueError(f"Record {record.name}: {err}")
        self.logger.info("End validating record %s", record.name)

    def reset(self):
        """Reset the validator to an initial state for record validation.

        Subclasses must override this method if any state is stored in
        the validator object.
        """

    def validate_record(self, record: Record):
        """Validate the entire record.

        This is called last in the validation process, so anything that
        would require all data items to be validated first should be
        checked here.
        """

    def validate_properties(self, record: Record):
        """Validate properties of the record.

        Subclasses should override this method if record properties
        need validation for content.
        """

    def validate_structured_data_aggregation(self, names: typing.Iterable[str]):
        """Validate that required structured data exists.

        Subclasses should override this method if specific named
        structured data is required (e.g. geographic structured data
        needs latitude and longitude).
        """

    def validate_structured_data(self, data: StructuredData):
        """Validate a single structured data item.

        Subclasses should override this method if values should have
        specific type or representation, or if other properties have
        limitations on values.
        """
        # pylint: disable=no-self-use
        if data.target not in Target:
            raise TypeError(f"StructuredData.target `{data.target}` is not a Target")
        if data.data_type not in DataType:
            raise TypeError(f"data_type `{data.data_type}` is not DataType")
        if data.data_type == DataType.CONTINUOUS:
            if not isinstance(data.value, (int, float)):
                raise ValueError(
                    f"StructuredData.value `{data.value}` is not continuous"
                )
        elif data.data_type == DataType.CATEGORY:
            pass
        else:
            raise ValueError(f"Unknown StructuredData.data_type `{data.data_type}`")

    def validate_unstructured_data(self, data: UnstructuredData):
        """Validate a single unstructured data item.

        Subclasses should override this method to validate the data
        property.
        """
        # pylint: disable=no-self-use
        if data.file_type not in FileType:
            raise TypeError(f"file_type `{data.file_type}` is not FileType")

        parts = urllib.parse.urlsplit(data.data_uri)
        if parts[0] == "file":
            value = "OK"
            path = pathlib.Path(urllib.parse.unquote(parts[2]))
            if not path.exists():
                value = "file missing"
            elif not path.is_file():
                value = "not a file"
            else:
                try:
                    path.open("r").close()
                except OSError as err:
                    value = str(err)
        elif parts[0] in ["http", "https"]:
            url = "https://docs.python.org/3/library/urllib.request.html"
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req)
            value = resp.reason
        else:
            value = f"Unknown URL scheme {parts[0]}"
        data.accessible = value
