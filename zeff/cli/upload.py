"""Zeff subcommand to upload records."""
__docformat__ = "reStructuredText en"
__all__ = ["upload_subparser"]

import logging
import zeff
import zeff.record
from .pipeline import subparser_pipeline, build_pipeline


def upload_subparser(subparsers, config):
    """Add the ``upload`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the upload sub-command.
    """

    parser = subparsers.add_parser("upload")
    subparser_pipeline(parser, config)
    parser.add_argument(
        "--no-train",
        action="store_true",
        help="""Build, validate, and upload training records, but do not
            start training of machine.""",
    )
    parser.set_defaults(func=upload)


def upload(options):
    """Generate a set of records from options."""
    counter, records = build_pipeline(options, zeff.Uploader)
    for record in records:
        logging.debug(record)
    if counter.count == 0 and not options.no_train:
        logging.debug("All records uploaded, start training.")
        trainer = zeff.Trainer()
        trainer.start()
