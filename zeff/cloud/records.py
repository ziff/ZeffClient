"""Zeff Cloud Datasets Records."""
__docformat__ = "reStructuredText en"

import json
from .resource import Resource
from .encoder import RecordEncoder


class Records(Resource):
    """Records access."""

    def __init__(self, datasetid, resource_map):
        super().__init__(resource_map)
        self.datasetid = datasetid

    def __iter__(self):
        """Return an iterator over all records in the dataset."""
        tag = "tag:zeff.com,2019-07:records/list"
        respjson = self.request(tag, datasetid=self.datasetid)
        return iter(respjson.get("data", []))

    def add(self, record):
        """Add a record to the dataset."""
        val = json.dumps(record, cls=RecordEncoder)
        print(val)
