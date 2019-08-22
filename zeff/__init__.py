# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
"""Zeff client library to Zeff Cloud API.

Zeff is a Python package that dimplifies the creation, modification,
and uploading of records to Zeff Cloud API.


Environment
===========


Loggers
=======

- ``zeffclient.record.builder``
    Logger that should be used by record builder's, including those
    made by users of ZeffClient.

- ``zeffclient.record.generator``
    Logger used by the record generation subsystem.

- ``zeffclient.record.validator``
    Logger used by the record validation subsystem.

- ``zeffclient.record.uploader``
    Logger used by the record upload subsystem.

"""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("ZeffClient").version
except pkg_resources.DistributionNotFound as err:
    __version__ = "0.0.0"


from .pipeline import Counter, record_builder_generator, validation_generator
from .pipeline_observation import *

# pylint: disable=duplicate-code

from .uploader import Uploader
from .predictor import Predictor
