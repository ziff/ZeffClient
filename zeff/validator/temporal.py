"""Zeff Validator."""
__docformat__ = "reStructuredText en"
__all__ = ["RecordTemporalValidator"]


import typing
import datetime
from .record import RecordValidator
from ..record import UnstructuredData, UnstructuredTemporalData, FileContext


class RecordTemporalValidator(RecordValidator):
    """Zeff Temporal Record Validator.

    This validator will check that required items are in a temporal
    record.

    .. WARNING::
        Only one record whould be validated at a time by a single
        validator object.
    """

    def validate_unstructured_data(self, data: UnstructuredData):
        """Validate a single unstructured data item.

        Subclasses should override this method to validate the data
        property.
        """
        # pylint: disable=no-self-use
        super().validate_unstructured_data(data)
        tdata = typing.cast(UnstructuredTemporalData, data)
        if tdata.temporal_window is None:
            raise ValueError("temporal_window must have a valid time value.")

        sctime = typing.cast(datetime.time, tdata.start_crop_time)
        ectime = typing.cast(datetime.time, tdata.end_crop_time)
        if sctime >= ectime:
            raise ValueError("start_crop_time must be before end_crop_time.")

        for filecontext in tdata.file_contexts:
            self.validate_filecontext(filecontext, 1)

    def validate_filecontext(self, filecontext: FileContext, maxdepth):
        """Validate a file context object.

        :parameter filecontext: The FileContext to validate.

        :parameter maxdepth: Allowed depth of encapsulated subcontexts.
            If this is 0 then subcontexts must be empty. This will
            be decreased on each recursive call of this method.
        """
        if maxdepth <= 0:
            ValueError("Depth of file context exceeds allowed amount.")
        if filecontext.start_time >= filecontext.end_time:
            ValueError("FileContext start_time must be before end_time.")
        for subcontext in filecontext.subcontexts:
            self.validate_filecontext(subcontext, (maxdepth - 1))
