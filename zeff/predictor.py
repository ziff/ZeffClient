"""Zeff build, and upload record for Zeff Cloud to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["Predictor"]

import logging
from .zeffcloud import ZeffCloudResourceMap
from .cloud.exception import ZeffCloudException, ZeffCloudModelException
from .cloud.dataset import Dataset
from .cloud.model import Model

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Predictor:
    """Upload a record to make prediction and report results.

    :param upstream: Generator of records to be uploaded.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    def __init__(self, upstream, server_url, org_id, user_id, dataset_id, version):
        """Create a generator that will use a record to infer a prediction.

        :param upstream: The upstream record generator.

        :param server_url: The URL to the server that has the model.

        :param org_id: Organization ID for authorization to the model.

        :param user_id: User ID for authorization to the model.

        :param dataset_id: The dataset ID that contains the model.

        :param version: The model version to make inferences against.
        """
        self.upstream = upstream

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=server_url, org_id=org_id, user_id=user_id
        )
        dataset = Dataset(dataset_id, self.resource_map)
        self.model = Model(dataset, version)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        while True:
            try:
                record = next(self.upstream)
                return self.model.add_record(record)
            except ZeffCloudException as err:
                LOGGER_UPLOADER.exception(err)
            except ZeffCloudModelException as err:
                LOGGER_UPLOADER.error(err)
                break
