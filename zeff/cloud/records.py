"""Zeff Cloud Datasets Records."""
__docformat__ = "reStructuredText en"

import logging
import json
import textwrap
from .resource import Resource
from .dataset import Dataset
from .encoder import RecordEncoder

LOGGER = logging.getLogger("zeffclient.record.uploader")


class Records(Resource):
    """Records access."""

    def __init__(self, dataset: Dataset, resource_map):
        """Initialize for record resource access.

        :param dataset: Dataset to use for all record access.

        :param resource_map: ZeffResourceMap for tag to URL mapping.
        """
        super().__init__(resource_map)
        self.dataset = dataset

    def __iter__(self):
        """Return an iterator over all records in the dataset."""
        tag = "tag:zeff.com,2019-07:records/list"
        resp = self.request(tag, dataset_id=self.dataset.dataset_id)
        return iter(resp.json().get("data", []))

    def add(self, record):
        """Add a record to the dataset."""
        LOGGER.info("Begin upload record %s", record.name)
        tag = "tag:zeff.com,2019-07:records/add"
        batch = {"batch": [record]}
        val = json.dumps(batch, cls=RecordEncoder)
        resp = self.request(
            tag, method="POST", data=val, dataset_id=self.dataset.dataset_id
        )
        if resp.status_code not in [200, 201]:
            LOGGER.error(
                "Error upload record %s: (%d) %s; %s",
                record.name,
                resp.status_code,
                resp.reason,
                resp.text,
            )
            return textwrap.dedent(
                f"""\
                Record {record.name} add failed {resp.status_code} -
                {resp.reason}: {resp.text}
                """
            ).replace("\n", " ")

        data = resp.json()["data"][0]
        LOGGER.info(
            """End upload record %s: recordId = %s location = %s""",
            record.name,
            data["recordId"],
            data["location"],
        )
        return textwrap.dedent(
            f"""\
            Record {data["uniqueName"]} created
            with {data["recordId"]}
            at {data["location"]}.
            """
        ).replace("\n", " ")
