"""Zeff test formatters."""

import pytest
from io import StringIO
from zeff.record import (
    Record,
    StructuredData,
    UnstructuredData,
    format_record_restructuredtext,
)


def test_format_record_restructuredtext():
    """TBW."""
    r = Record("Formatted Record")

    sd_info = [
        (
            "sold_price",
            1368411.0,
            StructuredData.DataType.CONTINUOUS,
            StructuredData.Target.NO,
        ),
        (
            "basement",
            2412.0,
            StructuredData.DataType.CONTINUOUS,
            StructuredData.Target.NO,
        ),
        (
            "garage_parking",
            "uncovered; rv parking; storage above; extra length; workbench",
            StructuredData.DataType.CATEGORY,
            StructuredData.Target.NO,
        ),
        (
            "lot",
            "auto-part; private",
            StructuredData.DataType.CATEGORY,
            StructuredData.Target.NO,
        ),
    ]
    for info in sd_info:
        sd = StructuredData(*info)
        sd.record = r

    ud_info = [
        ("https://www.example.com/properties/photo_5.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_37.jpg", "image/jpg", "home_photo"),
        ("https://www.example.com/properties/photo_6.jpg", "image/jpg", "home_photo"),
    ]
    for info in ud_info:
        ud = UnstructuredData(*info)
        ud.record = r

    result = StringIO()
    format_record_restructuredtext(r, out=result)
