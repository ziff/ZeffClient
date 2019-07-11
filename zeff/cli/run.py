"""Zeff subcommand to run a record generator."""
__docformat__ = "reStructuredText en"
__all__ = ["run_subparser"]

import sys
import os
import logging
import urllib
import errno
import importlib

import zeff
import zeff.record


def run_subparser(subparsers):
    """Add the ``run`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the run sub-command.
    """

    def create_url(argstr):
        parts = urllib.parse.urlsplit(argstr)
        if not parts.scheme:
            argstr = urllib.parse.urlunsplit(("file", "", argstr, "", ""))
        return argstr

    parser = subparsers.add_parser("run")
    parser.add_argument(
        "record-builder",
        help="Name of python class that will build a record given a URL to record sources.",
    )
    parser.add_argument(
        "--record-url-generator",
        default="zeff.recordgenerator.entry_url_generator",
        help="""Name of python class that will generate URLs to record
            sources (default: generates a URL for each entry in base
            directory.""",
    )
    parser.add_argument(
        "--records-base",
        dest="url",
        type=create_url,
        default=os.getcwd(),
        help="Base URL for records (default: current working directory)",
    )
    parser.add_argument(
        "--dry-run",
        choices=["configuration", "build", "validate"],
        help="""Do a dry run up to the specified phase and print
            results to stdout.""",
    )
    parser.set_defaults(func=run)


def run(options):
    """Generate a set of records from options."""

    def get_mclass(name):
        try:
            path = getattr(options, name)
            logging.debug("Look for %s: `%s`", name, path)
            m_name, c_name = path.rsplit(".", 1)
            module = importlib.import_module(m_name)
            logging.debug("Found module `%s`", m_name)
            return getattr(module, c_name)
        except ModuleNotFoundError:
            print(
                f"{name} module `{m_name}` not found in PYTHONPATH={sys.path}",
                file=sys.stderr,
            )
            sys.exit(errno.EINVAL)
        except AttributeError:
            print(f"{name} class `{c_name}` not found in {m_name}", file=sys.stderr)
            sys.exit(errno.EINVAL)

    record_url_generator = get_mclass("record_url_generator")
    logging.debug("Found record-url-generator: %s", record_url_generator)

    record_builder = get_mclass("record-builder")
    logging.debug("Found record-builder: %s", record_builder)

    if options.dry_run == "configuration":
        zeff.runner(record_url_generator(options.url), print, lambda r: r, lambda r: r)
    elif options.dry_run == "build":
        zeff.runner(
            record_url_generator(options.url), record_builder, lambda r: r, lambda r: r
        )
    elif options.dry_run == "validate":
        zeff.runner(
            record_url_generator(options.url),
            record_builder,
            lambda r: zeff.record.Record.validate,
            lambda r: r,
        )
    else:
        zeff.runner(
            record_url_generator(options.url),
            record_builder,
            lambda r: zeff.record.Record.validate,
            lambda r: print("Uploader not built"),
        )
