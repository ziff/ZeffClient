"""Zeff commandline processing utilities."""
__docformat__ = "reStructuredText en"

import logging
import zeff
import zeff.record
from .server import subparser_server
from .actions import NamedClassObjectAction, NamedCallableObjectAction


def subparser_pipeline(parser, config):
    """Add CLI arguments necessary for pipeline."""

    parser.add_argument(
        "--records-datasetid",
        default=config.records.datasetid,
        help="""Dataset id to use with records.""",
    )
    parser.add_argument(
        "--records-config-generator",
        action=NamedCallableObjectAction,
        default=config.records.records_config_generator,
        help=f"""Name of python class that will generate URLs to record
            sources (default: `%(default)s`)""",
    )
    parser.add_argument(
        "--records-config-arg",
        default=config.records.records_config_arg,
        help=f"""A single argument when records-config-generator is created
            (default: `%(default)s`)""",
    )
    parser.add_argument(
        "--record-builder",
        action=NamedClassObjectAction,
        default=config.records.record_builder,
        help=f"""Name of python class that will build a record
            (default: `%(default)s`)""",
    )
    parser.add_argument(
        "--record-builder-arg",
        default=config.records.record_builder_arg,
        help=f"""A single argument when record-builder is created
            (default: `%(default)s`)""",
    )
    parser.add_argument(
        "--record-validator",
        action=NamedClassObjectAction,
        default=config.records.record_validator,
        help=f"""Name of python class that will validate a record
            (default: `%(default)s`)""",
    )

    subparser_server(parser, config)
    parser.add_argument(
        "--dry-run",
        choices=["configuration", "build", "validate"],
        help="""Dry run to specified phase with no changes to Zeff Cloud,
            and print results to stdout.""",
    )


def build_pipeline(options, model, zeffcloud, *args, **kwargs):
    """Build a record upload pipeline based on CLI options.

    :param options: Command line options.

    :param model: The pipeline is for a model record versus a dataset
        record. A model record is used for prediction, and a dataset
        record is used for training.

    :param zeffcloud: An upload generator that takes a record builder
        generator as the first parameter.

    :param *args: Additional positional arguments to give to ``zeffcloud``
        generator.

    :param **kwargs: Additional key word arguments to give to ``zeffcloud``
        generator.

    :return: A tuple of Counter and last generator in pipeline. The
        counter counts the number of configuration records generated.
    """

    config = options.configuration

    record_config_generator = config.records.records_config_generator
    logging.debug("Found record-config-generator: %s", record_config_generator)
    generator = record_config_generator(config.records.records_config_arg)
    counter = zeff.Counter(generator)
    generator = counter
    if options.dry_run == "configuration":
        return counter, generator

    record_builder = options.configuration.records.record_builder
    logging.debug("Found record-builder: %s", record_builder)
    generator = zeff.record_builder_generator(
        model, generator, record_builder(config.records.record_builder_arg)
    )
    if options.dry_run == "build":
        return counter, generator

    record_validator = config.records.record_validator
    logging.debug("Found record-validator: %s", record_validator)
    generator = zeff.validation_generator(generator, record_validator(model))
    if options.dry_run == "validate":
        return counter, generator

    generator = zeffcloud(
        generator,
        options.server_url,
        options.org_id,
        options.user_id,
        options.records_datasetid,
        *args,
        **kwargs,
    )
    return counter, generator
