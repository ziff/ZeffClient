"""Zeff Cloud Datasets Record."""
__docformat__ = "reStructuredText en"

import logging
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
        self.dataset_id = None
        self.record_id = None

        tag = "tag:zeff.com,2019-07:records"
        resp = self.request(tag, dataset_id=dataset.dataset_id, record_id=record_id)
        if resp.status_code not in [200]:
            LOGGER.error(
                "Error loading record %s: (%d) %s; %s",
                record_id,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise ZeffCloudException(resp, type(self), record_id, "load")
        data = resp.json()["data"]
        self.__dict__.update({Resource.snake_case(k): v for k, v in data.items()})
        assert self.dataset_id == dataset.dataset_id
        assert self.record_id == record_id
