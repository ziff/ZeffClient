# -*- coding: UTF-8 -*-
"""
Zeff is a commandline tool for working with Zeff Cloud API.

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

    ``-v --verbose {{critical,error,warning,info,debug}}``
        Change the logging level of the handler named ``console`` from
        the logging configuration file. This has no effect on any other
        handler or logger.

    ``--logging-conf``
        Custom logging configuration file using Python logging
        dictionary configuration.


Exit Status
===========
The following exit values shall be returned:

0
    Successful completion.

>0
    An error occurred (Standard errors from <errno.h>).

**********
References
**********

.. [RFC2119] RFC2119, Key words for use in RFCs to Indicate Requirement
    Levels, S. Bradner, March 1997.

.. [RFC3986] RFC3986, Uniform Resource Identifier (URI): Generic Syntax,
    T. Berners-Lee, R. Fielding, L. Masinter, January 2005.

.. [RFC5424] RFC5424, The Syslog Protocol, R. Gerhards, March 2009.
"""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"
__version__ = "0.0.0"

import sys
import pathlib
import argparse

from .template import *
from .generate import *
from .formatter import *


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
    generate_subparser(subparsers)
    template_subparser(subparsers)

    options = parser.parse_args(args=args)
    if not hasattr(options, "func"):
        parser.print_help()
        sys.exit(1)
    if options.verbose == "debug":
        print("Working directory:", pathlib.Path.cwd(), file=sys.stderr)
    return options
