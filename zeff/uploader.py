"""Zeff upload records to Zeff Cloud dataset."""
__docformat__ = "reStructuredText en"
__all__ = ["Uploader"]

import logging
from .zeffcloud import ZeffCloudResourceMap
from .cloud.exception import ZeffCloudException
from .cloud.dataset import Dataset

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Uploader:
    """Generator that will yield successfully uploaded records."""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    def __init__(self, upstream, server_url, org_id, user_id, dataset_id):
        """Create new uploader.

        :param upstream: Generator of records to be uploaded.

        :param server_url: Root URL to the Zeff Cloud API server.

        :param org_id: The organization id for authorization access.

        :param user_id: The user id for authorization access.

        :param dataset_id: The dataset id that all uploads will be sent to.
        """
        self.server_url = server_url
        self.org_id = org_id
        self.user_id = user_id
        self.dataset_id = dataset_id
        self.upstream = upstream

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=server_url, org_id=org_id, user_id=user_id
        )
        self.dataset = Dataset(self.dataset_id, self.resource_map)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        while True:
            try:
                record = next(self.upstream)
                return self.dataset.add_record(record)
            except ZeffCloudException as err:
                LOGGER_UPLOADER.exception(err)
