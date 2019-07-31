"""Zeff CLI test suite."""

import sys
import os
import io
import types
from . import chdir

import zeff.cli
from zeff.cli.upload import upload
from zeff.cli.train import train
from zeff.cli.predict import predict


def test_upload_generate(chdir):
    args = [
        "upload",
        "--no-train",
        "--dry-run=validate",
        "tests.zeffcliTestSuite.builder.HousePriceRecordBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve upload


def test_train_generate():
    # TODO: this needs to watch a mock ZeffCloud object
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(action="start")
    strio = io.StringIO()
    sys.stdout = strio
    train(options)


def test_predict_generate(chdir):
    args = [
        "predict",
        "--dry-run=validate",
        "tests.zeffcliTestSuite.builder.HousePriceRecordBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve predict
