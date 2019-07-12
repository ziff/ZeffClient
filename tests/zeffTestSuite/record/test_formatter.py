"""Zeff test formatters."""

import pytest
from io import StringIO
from zeff.record import (
    Record,
    StructuredData,
    StructuredDataItem,
    UnstructuredData,
    UnstructuredDataItem,
    format_record_restructuredtext,
)


def test_format_record_restructuredtext():
    """TBW."""
    r = Record("Formatted Record")
    StructuredData().record = r
    UnstructuredData().record = r

    sd_info = [
        (
            "sold_price",
            1368411.0,
            StructuredDataItem.DataType.CONTINUOUS,
            StructuredDataItem.Target.NO,
        ),
        (
            "basement",
            2412.0,
            StructuredDataItem.DataType.CONTINUOUS,
            StructuredDataItem.Target.NO,
        ),
        (
            "garage_parking",
            "uncovered; rv parking; storage above; extra length; workbench",
            StructuredDataItem.DataType.CATEGORY,
            StructuredDataItem.Target.NO,
        ),
        (
            "lot",
            "auto-part; private",
            StructuredDataItem.DataType.CATEGORY,
            StructuredDataItem.Target.NO,
        ),
    ]
    for info in sd_info:
        sdi = StructuredDataItem(*info)
        sdi.structured_data = list(r.structured_data)[0]

    ud_info = [
        ("https://www.example.com/properties/photo_5.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_37.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_6.jpg", "image/jpg", "home_photo"),
    ]
    for info in ud_info:
        udi = UnstructuredDataItem(*info)
        udi.unstructured_data = list(r.unstructured_data)[0]

    result = StringIO()
    format_record_restructuredtext(r, out=result)
