"""Zeff Cloud Dataset access."""
__docformat__ = "reStructuredText en"

import logging
import json
from typing import Iterator
from .exception import ZeffCloudException
from .resource import Resource
from .training import TrainingSessionInfo


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
            raise ZeffCloudException(resp, type(self), dataset_id, "load")
        data = resp.json()["data"]
        self.__dict__.update({Resource.snake_case(k): v for k, v in data.items()})
        assert self.dataset_id == dataset_id

    def models(self):
        """Return iterator over all models in the dataset.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        from .model import Model

        tag = "tag:zeff.com,2019-07:models/list"
        resp = self.request(tag, dataset_id=self.dataset_id)
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), self.dataset_id, "list models")
        return (Model(self, d["version"]) for d in resp.json().get("data", []))

    def records(self):
        """Return iterator over all records in the dataset.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        from .record import Record

        tag = "tag:zeff.com,2019-07:records/list"
        resp = self.request(tag, dataset_id=self.dataset_id)
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), self.dataset_id, "list records")
        return (Record(self, d["recordId"]) for d in resp.json().get("data", []))

    def add_record(self, record):
        """Add a record to this dataset.

        :param record: The record data structure to be added.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        from .record import Record

        tag = "tag:zeff.com,2019-07:records/add"
        data = self.add_resource(record, record.name, "recordId", tag)
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
        tag = "tag:zeff.com,2019-07:datasets/train"
        resp = self.request(tag, method="DELETE", dataset_id=self.dataset_id)
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), self.dataset_id, "training stop")
