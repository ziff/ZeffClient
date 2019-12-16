"""Zeff subcommand to upload records."""
__docformat__ = "reStructuredText en"
__all__ = ["upload_subparser"]

import logging
import zeff
import zeff.record
from .pipeline import subparser_pipeline, build_pipeline
from .train import Trainer


def upload_subparser(subparsers, config):
    """Add the ``upload`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the upload sub-command.
    """

    parser = subparsers.add_parser(
        "upload", help="""Build, validate, and upload training records."""
    )
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
    logger = logging.getLogger("zeffclient.record.uploader")
    logger.info("Build upload pipeline")
    counter, records = build_pipeline(options, False, zeff.Uploader)
    logger.info("Upload pipeline starts")
    for record in records:
        logger.info("Record Count %d", counter.count)
        logger.debug(record)
    logger.info("Upload pipeline completes")
    logging.info("Records uploaded %d", counter.count)
    if counter.count == 0 and not options.no_train:
        logger.info("Start training the model")
        logger.debug("All records uploaded, start training.")
        trainer = Trainer(options)
        trainer.start()
    logger.info("Upload process completes")
