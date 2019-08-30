"""Zeff Cloud Datasets Record."""
__docformat__ = "reStructuredText en"

import logging
import datetime
from .exception import ZeffCloudException
from .resource import Resource

LOGGER = logging.getLogger("zeffclient.record.uploader")


class Record(Resource):
    """Zeff Cloud Record access."""

    def __init__(self, dataset, record_id: str):
        """Initialize a record resource access.

        :param dataset: The containing Dataset.

        :param record_id: The unique recordId of the record in the Zeff
            Cloud API.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        super().__init__(dataset.resource_map)
        self.dataset = dataset
        self.__record_id = record_id
        self.update()

    def __str__(self):
        """Return user friendly representation."""
        return f"<Record dataset:{self.dataset_id} record:{self.record_id}>"

    def update(self):
        """Update record information from Zeff Cloud."""
        tag = "tag:zeff.com,2019-07:records"
        resp = self.request(
            tag, dataset_id=self.dataset.dataset_id, record_id=self.__record_id
        )
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), self.__record_id, "load")
        self.__data = resp.json()["data"]
        assert self.dataset_id == self.dataset.dataset_id
        assert self.record_id == self.__record_id

    @property
    def dataset_id(self):
        """Return dataset id for this record."""
        return self.__data["datasetId"]

    @property
    def record_id(self):
        """Return this record's id."""
        return self.__data["recordId"]

    @property
    def structured_data(self):
        """Return the structured data list for this record."""
        return self.__data["recordData"]["structuredData"]

    @property
    def unstructured_data(self):
        """Return the unstructured data list for this record."""
        return self.__data["recordData"]["unstructuredData"]

    @property
    def created_timestamp(self) -> datetime.datetime:
        """Return the timestamp when this record was created."""
        value = self.__data["createdAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = datetime.datetime.min
        return ret

    @property
    def updated_timestamp(self) -> datetime.datetime:
        """Return the timestamp when this record was updated."""
        value = self.__data["updatedAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = datetime.datetime.min
        return ret

    @property
    def predictions(self):
        """Return predictions for this record."""
        return self.__data["predictions"]

    @property
    def errors(self):
        """Return errors for this record."""
        return self.__data["errors"]
