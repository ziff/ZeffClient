"""Zeff test suite."""

import os
import pathlib
import urllib.parse
import pytest

from zeff.recordgenerator import entry_generator, file_generator, directory_generator


def test_entries():
    path = pathlib.Path.cwd()
    entries = [p.name for p in path.iterdir() if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in entry_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0


def test_file_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_file()]
    entries = [p.name for p in entries if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in file_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0


def test_dir_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_dir()]
    entries = [p.name for p in entries if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in directory_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0
