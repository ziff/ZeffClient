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
import argparse

from .template import *
from .run import *


def parse_commandline(args=None):
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
    run_subparser(subparsers)
    template_subparser(subparsers)

    options = parser.parse_args(args=args)
    if not hasattr(options, "func"):
        parser.print_help()
        sys.exit(1)
    if options.verbose == "debug":
        print("Working directory:", pathlib.Path.cwd(), file=sys.stderr)
    return options
