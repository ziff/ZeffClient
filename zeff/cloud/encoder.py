"""Zeff CLI record encoders."""
__docformat__ = "reStructuredText en"


import json
from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    UnstructuredTemporalData,
    FileContext,
)


class RecordEncoder(json.JSONEncoder):
    """Encode Zeff Records."""

    # pylint: disable=method-hidden

    def default(self, o):
        """Return primative objects for Record."""
        # pylint: disable=no-else-return
        if isinstance(o, Record):
            ret = {}
            ret["name"] = {
                "uniqueName": str(o.name),
                "sortAscending": True,
                "holdoutRecord": True,
            }
            if len(o.structured_data) > 0:
                ret["structuredData"] = o.structured_data
            if len(o.unstructured_data) > 0:
                ret["unstructuredData"] = o.unstructured_data
            return ret
        elif isinstance(o, StructuredData):
            return {
                "name": o.name,
                "value": o.value,
                "dataType": o.data_type.name,
                "target": o.target.name,
            }
        elif isinstance(o, UnstructuredTemporalData):
            raise NotImplementedError()
            # return {
            #     "data": o.data_uri,
            #     "fileType": o.file_type.name,
            #     "groupByName": o.group_by,
            # }
        elif isinstance(o, UnstructuredData):
            return {
                "data": o.data_uri,
                "fileType": o.file_type.name,
                "groupByName": o.group_by,
            }
        elif isinstance(o, FileContext):
            raise NotImplementedError()
        else:
            return super().default(o)
