"""Zeff Validator."""
__docformat__ = "reStructuredText en"
__all__ = ["RecordGenericValidator"]

from .record import RecordValidator

# from ..record import (
#     StructuredData,
#     UnstructuredData,
# )


class RecordGenericValidator(RecordValidator):
    """Zeff Generic Record Validator.

    This validator will check that required items are in a generic
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """
