"""Zeff Cloud training status."""
__docformat__ = "reStructuredText en"

import enum
import datetime
import logging
import json


class TrainingStatus(enum.Enum):
    """Model training status."""

    unknown = "UNKNOWN"
    queued = "QUEUED"
    started = "STARTED"
    progress = "PCT_COMPLETE"
    complete = "COMPLETE"

    def __str__(self):
        """Return a user appropriate name of this status."""
        return self.name

    def __repr__(self):
        """Return a representation of this status."""
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class TrainingSessionInfo:
    """Information about the current training session."""

    def __init__(self, status_json):
        """Create a new training information.

        :param status_json: The status JSON returned from a train
            status request.
        """
        self.__data = status_json
        logging.debug("Training Session JSON: \n%s", self.__data_str())

    def __data_str(self):
        """Return the data as a JSON formatted string."""
        return json.dumps(self.__data, indent="\t", sort_keys=True)

    @property
    def status(self) -> TrainingStatus:
        """Return state of current training session."""
        value = self.__data["status"]
        return TrainingStatus(value if value is not None else "UNKNOWN")

    @property
    def progress(self) -> float:
        """Return progress, [0.0, 1.0], of current training session."""
        value = self.__data["percentComplete"]
        return float(value) if value is not None else 0.0

    @property
    def model_version(self) -> str:
        """Return model version of the current training session."""
        value = self.__data["modelVersion"]
        return str(value) if value is not None else "unknown"

    @property
    def model_location(self) -> str:
        """Return the URL to the model."""
        value = self.__data["modelLocation"]
        return str(value) if value is not None else "unknown"

    @property
    def created_timestamp(self) -> datetime.datetime:
        """Return the timestamp when this training session was created."""
        value = self.__data["createdAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = datetime.datetime.min
        return ret

    @property
    def updated_timestamp(self) -> datetime.datetime:
        """Return timestamp when current session status was last updated."""
        value = self.__data["updatedAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = self.created_timestamp
        return ret
