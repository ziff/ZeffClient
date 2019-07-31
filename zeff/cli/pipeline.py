"""Zeff commandline processing utilities."""
__docformat__ = "reStructuredText en"

import sys
import logging
import errno
import importlib

import zeff
import zeff.record
from .server import subparser_server


def subparser_pipeline(parser, config):
    """Add CLI arguments necessary for pipeline."""

    parser.add_argument(
        "records-builder",
        help="Name of python class that will build a record given a URL to record sources.",
    )
    parser.add_argument(
        "--records-datasetid",
        default=config["records"]["datasetid"],
        help="""Dataset id use with records.""",
    )
    parser.add_argument(
        "--records-config-generator",
        default=config["records"]["config_generator"],
        help=f"""Name of python class that will generate URLs to record
            sources (default: {config["records"]["config_generator"]})""",
    )
    parser.add_argument(
        "--records-config-url",
        default=config["records"]["config_url"],
        help=f"""URL or localpath as the single argument to a
            record-config-generator
            (default: `{config["records"]["config_url"]}`)""",
    )
    subparser_server(parser, config)
    parser.add_argument(
        "--dry-run",
        choices=["configuration", "build", "validate"],
        help="""Dry run to specified phase with no changes to Zeff Cloud,
            and print results to stdout.""",
    )


def build_pipeline(options, zeffcloud):
    """Build a record upload pipeline based on CLI options.

    :param options: Command line options.

    :param zeffcloud: An upload generator that takes a record builder
        generator as the first parameter.

    :return: A tuple of Counter and last generator in pipeline. The
        counter counts the number of configuration records generated.
    """

    def get_mclass(name):
        path = getattr(options, name)
        logging.debug("Look for %s: `%s`", name, path)
        m_name, c_name = path.rsplit(".", 1)
        try:
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

    record_config_generator = get_mclass("records_config_generator")
    logging.debug("Found record-config-generator: %s", record_config_generator)
    generator = record_config_generator(options.records_config_url)
    counter = zeff.Counter(generator)
    generator = counter
    if options.dry_run == "configuration":
        return counter, generator

    records_builder = get_mclass("records-builder")
    logging.debug("Found records-builder: %s", records_builder)
    generator = zeff.record_builder_generator(generator, records_builder())
    if options.dry_run == "build":
        return counter, generator

    generator = zeff.validation_generator(generator)
    if options.dry_run == "validate":
        return counter, generator

    generator = zeffcloud(
        generator,
        options.server_url,
        options.org_id,
        options.user_id,
        options.records_datasetid,
    )
    return counter, generator
