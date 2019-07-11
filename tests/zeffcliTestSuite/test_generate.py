"""Zeff CLI test suite."""

import sys
import os
import io
import types

from zeff.cli.run import run


def test_generate():
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
    run(options)
    sys.stdout = sys.__stdout__

    urls = [url.strip() for url in strio.getvalue().split("\n") if url]
    names = [os.path.basename(url) for url in urls]
    names.sort()

    files = os.listdir(dirpath)
    files.sort()

    assert names == files
