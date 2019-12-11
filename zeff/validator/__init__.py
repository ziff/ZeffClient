"""ZeffClient Validator.

A validator is a filtering generator that will check each record's state
to ensure that it is valid for the type of record (e.g. geolocation
record structured data needs to have latitude and longitude entries).

"""
__docformat__ = "reStructuredText en"

from .record import *
from .generic import *
from .temporal import *
from .geospatial import *
