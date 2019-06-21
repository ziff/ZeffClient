# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
"""ZeffLib test suite."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

import unittest
from unittest.mock import Mock
import logging
from zefflib.reporter import LoggingReporter

class LoggingReporterTestCase(unittest.TestCase):

    def setUp(self):
        self.mock = Mock(spec=logging.Handler)
        self.mock.level = logging.DEBUG
        self.logger = logging.Logger("TEST_LOGGER")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.mock)

        self.record = "TEST RECORD"
        self.error = ValueError("TEST EXECEPTION")

    def test_generated(self):
        """Generated record is logged to logger INFO level."""

        sut = LoggingReporter(self.logger)
        sut.generated(self.record)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.INFO)
        self.assertEqual(record.args[0], self.record)


    def test_validate_success(self):
        """Validated record is logged to logger INFO level."""

        sut = LoggingReporter(self.logger)
        sut.validate_success(self.record)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.INFO)
        self.assertEqual(record.args[0], self.record)


    def test_validate_warning(self):
        """Validation warning is logged to logger WARNING level."""

        sut = LoggingReporter(self.logger)
        sut.validate_warning(self.record, self.error)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.WARNING)
        self.assertEqual(record.args[0], self.record)
        self.assertEqual(record.args[1], self.error)


    def test_validate_error(self):
        """Validation error is logged to logger ERROR level."""

        sut = LoggingReporter(self.logger)
        sut.validate_error(self.record, self.error)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.ERROR)
        self.assertEqual(record.args[0], self.record)
        self.assertEqual(record.args[1], self.error)


    def test_submit_success(self):
        """Submit success is logged to logger INFO level."""

        sut = LoggingReporter(self.logger)
        sut.submit_success(self.record)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.INFO)
        self.assertEqual(record.args[0], self.record)


    def test_submit_error(self):
        """Submit error is logged to logger ERROR level."""

        sut = LoggingReporter(self.logger)
        sut.submit_error(self.record, self.error)

        self.mock.handle.assert_called()
        record = self.mock.handle.call_args[0][0]
        self.assertEqual(record.levelno, logging.ERROR)
        self.assertEqual(record.args[0], self.record)
        self.assertEqual(record.args[1], self.error)


