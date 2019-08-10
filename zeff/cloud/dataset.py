"""Zeff Cloud Dataset access."""
__docformat__ = "reStructuredText en"

import logging
import json
import re
from typing import Iterator
from .resource import Resource


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

        :raises [ErrorType]:
        """
        resource = Resource(resource_map)
        tag = "tag:zeff.com,2019-07:datasets/add"
        body = {"title": title, "description": description}
        resp = resource.request(tag, method="POST", data=json.dumps(body))
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

        :raises [ErrorType]:
        """

        def snake_case(name):
            name = re.sub(r"([A-Z])", r"_\1", name).lstrip("_")
            name = name.lower()
            return name

        super().__init__(resource_map)
        self.dataset_id = None
        tag = "tag:zeff.com,2019-07:datasets"
        resp = self.request(tag, dataset_id=dataset_id)
        data = resp.json()["data"]
        self.__dict__.update({snake_case(k): v for k, v in data.items()})
        assert self.dataset_id == dataset_id
