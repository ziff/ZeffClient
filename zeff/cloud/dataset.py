"""Zeff Cloud Dataset access."""
__docformat__ = "reStructuredText en"

import logging
import enum
import json
import datetime
from typing import Iterator
from .exception import ZeffCloudException
from .resource import Resource
from .encoder import RecordEncoder


LOGGER = logging.getLogger("zeffclient.record.uploader")


class Dataset(Resource):
    """Dataset in the Zeff Cloud API."""

    @classmethod
    def create_dataset(cls, resource_map, title: str, description: str) -> "Dataset":
        """Create a new dataset on Zeff Cloud server.

        :param resource_map: Map of tags to Zeff Cloud resource objects.

        :param title: Title of the new dataset.

        :param description: Description of the new dataset.

        :param temporal: Type of dataset to create.

        :return: A Dataset which maps to the instance in Zeff Cloud.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        resource = Resource(resource_map)
        tag = "tag:zeff.com,2019-07:datasets/add"
        body = {"title": title, "description": description}
        resp = resource.request(tag, method="POST", data=json.dumps(body))
        if resp.status_code not in [201]:
            LOGGER.error(
                "Error creating dataset %s: (%d) %s; %s",
                title,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise ZeffCloudException(resp, cls, title, "create")
        data = resp.json()["data"]
        assert data["title"] == title
        dataset_id = data["datasetId"]
        return cls(dataset_id, resource_map)

    @classmethod
    def datasets(cls) -> Iterator["Dataset"]:
        """Return iterator of all datasets in Zeff Cloud server."""

    def __init__(self, dataset_id: str, resource_map):
        """Load a dataset from Zeff Cloud server.

        :param dataset_id: This maps to the datasetId for a dataset record
            in the Zeff Cloud API.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        super().__init__(resource_map)
        self.dataset_id = None
        tag = "tag:zeff.com,2019-07:datasets"
        resp = self.request(tag, dataset_id=dataset_id)
        if resp.status_code not in [200]:
            LOGGER.error(
                "Error loading dataset %s: (%d) %s; %s",
                dataset_id,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise ZeffCloudException(resp, type(self), dataset_id, "load")
        data = resp.json()["data"]
        self.__dict__.update({Resource.snake_case(k): v for k, v in data.items()})
        assert self.dataset_id == dataset_id

    def records(self):
        """Return iterator over all records in the dataset.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        tag = "tag:zeff.com,2019-07:records/list"
        resp = self.request(tag, dataset_id=self.dataset_id)
        if resp.status_code not in [200]:
            LOGGER.error(
                "Error listing dataset records %s: (%d) %s; %s",
                self.dataset_id,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise ZeffCloudException(resp, type(self), self.dataset_id, "list records")
        return iter(resp.json().get("data", []))

    def add_record(self, record):
        """Add a record to this dataset.

        :param record: The record data structure to be added.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        from .record import Record

        LOGGER.info("Begin upload record %s", record.name)
        tag = "tag:zeff.com,2019-07:records/add"
        batch = {"batch": [record]}
        val = json.dumps(batch, cls=RecordEncoder)
        resp = self.request(tag, method="POST", data=val, dataset_id=self.dataset_id)
        if resp.status_code not in [200, 201]:
            LOGGER.error(
                "Error upload record %s: (%d) %s; %s",
                record.name,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise ZeffCloudException(resp, type(self), record.name, "add record")
        data = resp.json()["data"][0]
        LOGGER.info(
            """End upload record %s: recordId = %s location = %s""",
            record.name,
            data["recordId"],
            data["location"],
        )
        return Record(self, data["recordId"])

    @property
    def training_status(self):
        """Return current training status metrics object."""
        tag = "tag:zeff.com,2019-07:datasets/train"
        resp = self.request(tag, method="GET", dataset_id=self.dataset_id)
        if resp.status_code not in [200]:
            raise ZeffCloudException(
                resp, type(self), self.dataset_id, "training status"
            )
        return TrainingSessionInfo(resp.json()["data"])

    def start_training(self):
        """Start or restart the current training session."""
        tag = "tag:zeff.com,2019-07:datasets/train"
        resp = self.request(tag, method="PUT", dataset_id=self.dataset_id)
        if resp.status_code not in [202]:
            raise ZeffCloudException(
                resp, type(self), self.dataset_id, "training start"
            )

    def stop_training(self):
        """Stop the current training session."""
        # pylint: disable=no-self-use
        logging.debug("Stop de training")

    def kill_training(self):
        """Kill the current training session and mark invalid."""
        # pylint: disable=no-self-use
        logging.debug("Kill the training session")


class TrainingSessionInfo:
    """Information about the current training session."""

    class State(enum.Enum):
        """Training state of training session."""

        unknown = "UNKNOWN"
        queued = "QUEUED"
        started = "STARTED"
        progress = "PCT_COMPLETE"
        complete = "COMPLETE"

        def __str__(self):
            """Return a user appropriate name of this state."""
            return self.name

        def __repr__(self):
            """Return a representation of this state."""
            return "<%s.%s>" % (self.__class__.__name__, self.name)

    def __init__(self, status_json):
        """Create a new training information.

        :param status_json: The status JSON returned from a train
            status request.
        """
        self.__data = status_json

    @property
    def status(self) -> "TrainingSessionInfo.State":
        """Return state of current training session."""
        value = self.__data["status"]
        return TrainingSessionInfo.State(value if value is not None else "unknown")

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
