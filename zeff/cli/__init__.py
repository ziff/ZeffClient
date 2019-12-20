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
        Change the root logger logging level and the root logger
        handler name ``console`` logging level. Other loggers and
        handlers are unchanged, but named loggers that use ``console``
        handler may emit more log information.


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


Logging
=======

Logging configuration will use either ``${PWD}/zeff_logging.conf``
or a default internal configuration.

Named Loggers
-------------

zeffclient.record.generator
    Used during the configuration generation stage as configuration
    strings are created.

zeffclient.record.builder
    Used during the builder stage as records are being built from the
    configuration string parameter.

zeffclient.record.validator
    Used during the validation stage as records are being validated.

zeffclient.record.uploader
    Used during the upload stage as records are being uploaded.


The single unamed root logger will have log messages that are not
associated with the generator, builder, validator, or uploader
stages.


Default Configuration
---------------------

The default configuration of the named loggers is to warning and higher
level log messages to the console, and will emit info and higher level
log messages associated named and dated log files in ``${PWD}/var/log``
(e.g. ``${PWD}/var/log/builder_2019-12-16T11:23:47.log`` if the log
file for the builder stage for an execution run that started on 16
Dec 2019 at 11:23:47 local time).

The named loggers and the root logger will emit log messages of debug
or higher level into a master log file in ``${PWD}/var/log``. The
master log file will be dated with the start date and time of the run.

The ``${PWD}/var/log`` directory may be removed at anytime: it will
be recreated on the next run of zeff.


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
import os
import errno
import logging
import logging.config
import datetime
import ast
import pathlib
import argparse

from zeff import __version__

from .configuration import *
from .init import *
from .models import *
from .upload import *
from .train import *
from .predict import *
from .record_builders import *


def configure_logging():
    """Configure the logging system.

    Configuration uses the Python logging dictionary schema. The
    schema will be read from either ``${PWD}/zeff_logging.conf``
    if it exists, or from ``logging_default.txt`` in the same
    directory as this source file.

    .. caution:: This method should be called before ``parse_commandline``.
    """

    try:
        path = pathlib.Path.cwd() / "zeff_logging.conf"
        with open(path, "r") as file:
            conf = ast.literal_eval(file.read())
            logging.config.dictConfig(conf)
    except OSError:
        try:
            package = pathlib.PurePosixPath(__file__).parent
            path = package / "logging_default.txt"
            with open(path, "r") as file:
                conf = ast.literal_eval(file.read())
            logdir = pathlib.Path.cwd() / "var" / "log"
            now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            def fixfilename(name):
                filename = f"{name}_{now}.log"
                path = logdir / filename
                conf["handlers"][name]["filename"] = path

            fixfilename("master")
            fixfilename("generator")
            fixfilename("builder")
            fixfilename("validator")
            fixfilename("uploader")
            os.makedirs(logdir, exist_ok=True)
            logging.config.dictConfig(conf)
        except OSError as err:
            print(f"Unable to configure logging: {err}", file=sys.stderr)
            sys.exit(errno.EIO)


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

    subparsers = parser.add_subparsers(help="sub-command help")
    init_subparser(subparsers)
    models_subparser(subparsers, config)
    upload_subparser(subparsers, config)
    train_subparser(subparsers, config)
    predict_subparser(subparsers, config)
    options = parser.parse_args(args=args)

    # Adjust root logger and console to match verbose
    rootlogger = logging.getLogger()
    rootlogger.setLevel(options.verbose.upper())
    rootconsole = [h for h in rootlogger.handlers if h.get_name() == "console"]
    if rootconsole:
        rootconsole = rootconsole[0]
        rootconsole.setLevel(options.verbose.upper())

    # Update configuration and set in options
    config.update(options)
    options.configuration = config
    if not hasattr(options, "func"):
        parser.print_help()
        sys.exit(1)
    if options.verbose == "debug":
        print("Working directory:", pathlib.Path.cwd(), file=sys.stderr)
    return options
