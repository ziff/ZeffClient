"""Zeff commandline processing utilities."""
__docformat__ = "reStructuredText en"

import sys
import os
import urllib
import logging
import errno
import importlib

import zeff
import zeff.record


def subparser_pipeline(parser):
    """Add CLI arguments necessary for pipeline."""

    def create_url(argstr):
        """Create file URL from argstr when used for argparse type."""
        parts = urllib.parse.urlsplit(argstr)
        if not parts.scheme:
            argstr = urllib.parse.urlunsplit(("file", "", argstr, "", ""))
        return argstr

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
        help="""Dry run to specified phase with no changes to Zeff Cloud,
            and print results to stdout.""",
    )


def build_pipeline(options, zeffcloud):
    """Build a record upload pipeline based on CLI options."""

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
        upload_success = zeff.pipeline(
            record_url_generator(options.url), print, lambda r: r, lambda r: r
        )
    elif options.dry_run == "build":
        upload_success = zeff.pipeline(
            record_url_generator(options.url), record_builder, lambda r: r, lambda r: r
        )
    elif options.dry_run == "validate":
        upload_success = zeff.pipeline(
            record_url_generator(options.url),
            record_builder(),
            lambda r: zeff.record.Record.validate,
            lambda r: r,
        )
    else:
        upload_success = zeff.pipeline(
            record_url_generator(options.url),
            record_builder(),
            lambda r: zeff.record.Record.validate,
            zeffcloud,
        )

    return upload_success
