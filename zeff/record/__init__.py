"""ZeffClient Record.

A record is a collection of information that will be used to train
a machine, or on which the machine may make an inferance. The information
is contained in sets of strutured and unstructured data.

Structured data is dictionary of key-value items where the value has
either a continuous type (e.g. integer or floating point) or a discrete
type. This data may be marked to use for training, for inference, or
to be ignored by the machine.

Unstructured data is a stream of data that has media-type (e.g.
image/jpeg or video/mpeg) and an optional tag that will group it with
other unstructured data.

.. uml:: uml/recordClassDiagram.uml
   :scale: 50 %
   :align: center
"""
__docformat__ = "reStructuredText en"
__all__ = [
    "Record",
    "StructuredData",
    "UnstructuredData",
    "UnstructuredTemporalData",
    "Target",
    "DataType",
    "FileType",
]

from .symbolic import *
from .record import *
from .structureddata import *
from .unstructureddata import *
from .unstructuredtemporaldata import *
from .file import *
from .formatter import *
