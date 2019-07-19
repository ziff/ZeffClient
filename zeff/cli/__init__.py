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
        Change the logging level of the handler named ``console`` from
        the logging configuration file. This has no effect on any other
        handler or logger.

    ``--logging-conf path``
        Custom logging configuration file using Python logging
        dictionary configuration.


Sub-commands
============

    ``run``
        Build, validate, and upload records to Zeff Cloud from generated
        strings. See ``zeff run --help`` for arguments.

    ``template``
        Create a record builder template.



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
__version__ = "0.0.0"

import sys
import pathlib
import configparser
import argparse

from .template import *
from .upload import *
from .train import *
from .predict import *
from .record_builders import *


def load_configuration():
    """Load configuration from standard locations.

    Configuration files will be loaded in the following order such that
    values in later files will override those in earlier files:

        1. ``/etc/zeff.conf``
        2. ``${HOME}/.config/zeff/zeff.conf``
        3. ``./zeff.conf``
    """
    config = configparser.ConfigParser()
    config.read(
        [
            pathlib.Path(__file__).parent / "configuration_default.conf",
            "/etc/zeff.conf",
            pathlib.Path.home() / ".config" / "zeff" / "zeff.conf",
            pathlib.Path.cwd() / ".zeff.conf",
        ]
    )
    return config


def parse_commandline(args=None, config=None):
    """Construct commandline parser and then parse arguments."""
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
    upload_subparser(subparsers, config)
    train_subparser(subparsers, config)
    predict_subparser(subparsers, config)
    template_subparser(subparsers)

    options = parser.parse_args(args=args)
    if not hasattr(options, "func"):
        parser.print_help()
        sys.exit(1)
    if options.verbose == "debug":
        print("Working directory:", pathlib.Path.cwd(), file=sys.stderr)
    return options
