"""Zeff Cloud Dataset access."""
__docformat__ = "reStructuredText en"

import logging
import json
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
