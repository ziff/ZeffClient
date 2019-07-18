"""Zeff CLI test suite."""

import sys
import os
import io
import types

from zeff.cli.upload import upload
from zeff.cli.train import train
from zeff.cli.predict import predict


def test_upload_generate():
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(
        record_url_generator="zeff.recordgenerator.entry_url_generator",
        url=f"file://{dirpath}",
        **{
            "record-builder": "tests.zeffcliTestSuite.TestRecordBuilder.TestRecordBuilder"
        },
        dry_run="configuration",
        no_train=False,
    )
    strio = io.StringIO()
    sys.stdout = strio
    upload(options)
    sys.stdout = sys.__stdout__

    urls = [url.strip() for url in strio.getvalue().split("\n") if url]
    names = [os.path.basename(url) for url in urls]
    names.sort()

    files = os.listdir(dirpath)
    files.sort()

    assert names == files


def test_train_generate():
    # TODO: this needs to watch a mock ZeffCloud object
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(action="start")
    strio = io.StringIO()
    sys.stdout = strio
    train(options)


def test_predict_generate():
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(
        record_url_generator="zeff.recordgenerator.entry_url_generator",
        url=f"file://{dirpath}",
        **{
            "record-builder": "tests.zeffcliTestSuite.TestRecordBuilder.TestRecordBuilder"
        },
        dry_run="configuration",
    )
    strio = io.StringIO()
    sys.stdout = strio
    predict(options)
    sys.stdout = sys.__stdout__

    urls = [url.strip() for url in strio.getvalue().split("\n") if url]
    names = [os.path.basename(url) for url in urls]
    names.sort()

    files = os.listdir(dirpath)
    files.sort()

    assert names == files
