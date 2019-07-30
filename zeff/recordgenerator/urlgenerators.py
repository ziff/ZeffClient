"""Zeff collection of URL Generators."""
import pathlib
import urllib

__all__ = ["entry_generator", "file_generator", "directory_generator"]

# To Do Generators
# 1. HTTP index URL generator


def entry_generator(dirpath, allow=lambda p: True):
    """URL generator of entries in a path.

    Given a directory this will generate a URL to each entry in the
    directory.

    :param dirpath: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.

    :param allow: A filter that accepts a ``pathlib.Path`` and returns
        ``True`` if it is acceptable: i.e. if only files are wanted then
        the using ``lambda p: p.is_file()`` would filter out any non-files.
    """
    dirpath = pathlib.Path(dirpath)
    for path in (p for p in dirpath.iterdir() if allow(p)):
        if path.name.startswith("."):
            continue
        url = urllib.parse.urlunsplit(("file", "", str(path), "", ""))
        yield url


def file_generator(dirpath):
    """URL generator of files in a path.

    Given a directory this will generate a URL to each file in the
    directory.

    :param dirpath: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.
    """
    for entry in entry_generator(dirpath, allow=lambda p: p.is_file()):
        yield entry


def directory_generator(dirpath):
    """URL generator of directories in a path.

    Each directory in the ``dirpath`` will be generated as a file
    scheme URL.

    :param dirpath: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.
    """
    for entry in entry_generator(dirpath, allow=lambda p: p.is_dir()):
        yield entry
