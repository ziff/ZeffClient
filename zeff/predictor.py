"""Zeff build, and upload record for Zeff Cloud to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["Predictor"]

import logging
from .zeffcloud import ZeffCloudResourceMap
from .cloud.records import Records

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Predictor:
    """Upload a record to make prediction and report results.

    :param upstream: Generator of records to be uploaded.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    def __init__(self, upstream, server_url, org_id, user_id, datasetid):
        """TBW."""
        self.server_url = server_url
        self.org_id = org_id
        self.user_id = user_id
        self.datasetid = datasetid
        self.upstream = upstream

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=server_url, org_id=org_id, user_id=user_id
        )
        self.cloud_records = Records(self.datasetid, self.resource_map)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        record = next(self.upstream)
        return self.cloud_records.add(record)
