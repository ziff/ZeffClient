# -*- coding: UTF-8 -*-
"""
Zeff commandline tool man page.

####
Zeff
####

*****
Usage
*****

Name
====
    zeff


Synopsis
========
    ``zeff``


Description
===========
    ``zeff`` simplifies experimentation with Zeff Cloud API.


Options
=======

    ``-h --help``
        Display help.

    ``--version``
        Show version for zeff.

    ``--verbose {{critical,error,warning,info,debug}}``
        Change the logging level of the handler named ``console``
        from the logging configuration file. This has no effect
        on any other handler or logger.

    ``--logging-conf path``
        Custom logging configuration file using Python logging
        dictionary configuration.


Sub-commands
============

    ``init``
        Setup a new project in the current directory.

    ``upload``
        Build, validate, and upload training records.

    ``train``
        Control training sessions.

    ``predict``
        Upload record to infer a prediction.


Configuration
=============

Configuration may be done through command line options or may be
set in configuration files that are read from standard locations
(``/etc/zeff.conf``, ``${HOME}/.config/zeff/zeff.conf``,
``${PWD}/zeff.conf``), if the file exists.


Exit Status
===========
The following exit values shall be returned:

0
    Successful completion.

>0
    An error occurred (Standard errors from <errno.h>).

"""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"


import sys
import errno
import pathlib
from configparser import ConfigParser, ExtendedInterpolation, ParsingError
import argparse

from zeff import __version__

from .configuration import *
from .init import *
from .models import *
from .upload import *
from .train import *
from .predict import *
from .record_builders import *


def parse_commandline(args=None, config=None):
    """Construct commandline parser and then parse arguments.

    :param args: Command line arguments to parse. If none are
        given then ``sys.argv`` is used by default.

    :param config: ``configparser.ConfigParser`` object that
        contains the initial configuration of the system. The
        default is to use ``load_configuration`` to get the
        default.

    :return: A namespace that contains attributes with values
        determined from ``config`` and then command line
        arguments.
    """

    if config is None:
        config = load_configuration()
    package = pathlib.PurePosixPath(__file__).parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--verbose",
        type=str,
        default="warning",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Change default logging verbosity.",
    )
    parser.add_argument(
        "--logging-conf",
        type=str,
        default=package.joinpath("logging_default.txt"),
        help="Logging configuration file.",
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    init_subparser(subparsers)
    models_subparser(subparsers, config)
    upload_subparser(subparsers, config)
    train_subparser(subparsers, config)
    predict_subparser(subparsers, config)

    options = parser.parse_args(args=args)
    config.update(options)
    options.configuration = config
    if not hasattr(options, "func"):
        parser.print_help()
        sys.exit(1)
    if options.verbose == "debug":
        print("Working directory:", pathlib.Path.cwd(), file=sys.stderr)
    return options
