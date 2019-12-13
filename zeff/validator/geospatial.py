"""Zeff Validator."""
__docformat__ = "reStructuredText en"
__all__ = ["RecordGeospatialValidator"]


import typing
from .generic import RecordGenericValidator


class RecordGeospatialValidator(RecordGenericValidator):
    """Zeff Geospatial Record Validator.

    This validator will check that required items are in a geospatial
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """

    def validate_structured_data_aggregation(self, names: typing.Iterable[str]):
        """Check that `latitude` and `longitude` are available."""
        if "latitude" not in names:
            raise ValueError("Missing latitude data item.")
        if "longitude" not in names:
            raise ValueError("Missing longitude data item.")
