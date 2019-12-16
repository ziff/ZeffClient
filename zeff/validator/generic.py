"""Zeff Validator."""
__docformat__ = "reStructuredText en"
__all__ = ["RecordGenericValidator"]

from .record import RecordValidator
from ..record import Record, StructuredData, UnstructuredData, Target


class RecordGenericValidator(RecordValidator):
    """Zeff Generic Record Validator.

    See RecordValidator.
    """

    def __init__(self, *argv, **kwargs):
        """See RecordValidator.__init__."""
        super().__init__(*argv, **kwargs)
        self.has_target = False

    def reset(self):
        """See RecordValidator.reset."""
        self.has_target = False

    def validate_record(self, record: Record):
        """See RecordValidator.validate_record."""
        if self.model:
            pass
        else:
            if len(record.structured_data) < 1:
                raise ValueError(
                    "Dataset record must have at least one StructuredData item."
                )
            if not self.has_target:
                raise ValueError(
                    "Record for dataset must have a target StructuredData item."
                )

    def validate_structured_data(self, data: StructuredData):
        """See RecordValidator.validate_structured_data."""
        super().validate_structured_data(data)
        if data.target == Target.YES:
            self.has_target = True

    def validate_unstructured_data(self, data: UnstructuredData):
        """See RecordValidator.validate_unstructured_data."""
        # pylint: disable=unidiomatic-typecheck
        super().validate_unstructured_data(data)
        if type(data) != UnstructuredData:
            raise ValueError("Subclass of UnstructuredData not allowed.")
