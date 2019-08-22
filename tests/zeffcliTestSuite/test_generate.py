"""Zeff CLI test suite."""

import sys
import os
import io
import types
import pathlib
from . import chdir
import pytest

import zeff.cli
from zeff.cli.upload import upload
from zeff.cli.train import train
from zeff.cli.predict import predict


def test_upload_generate(chdir):
    args = [
        "upload",
        "--no-train",
        "--dry-run=validate",
        "--records-config-generator=tests.zeffcliTestSuite.generator.HousePriceRecordGenerator",
        f"--records-config-arg={pathlib.Path.cwd() / 'db.sqlite3'}",
        "--record-builder=tests.zeffcliTestSuite.builder.HousePriceRecordBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve upload


@pytest.mark.skip(reason="Need mock Zeff Cloud to test")
def test_train_generate():
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(action="start")
    strio = io.StringIO()
    sys.stdout = strio
    train(options)


def test_predict_generate(chdir):
    args = [
        "predict",
        "--dry-run=validate",
        "--records-config-generator=tests.zeffcliTestSuite.generator.HousePriceRecordGenerator",
        f"--records-config-arg={pathlib.Path.cwd() / 'db.sqlite3'}",
        "--record-builder=tests.zeffcliTestSuite.builder.HousePriceRecordBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve predict
