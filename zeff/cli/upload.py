"""Zeff subcommand to upload records."""
__docformat__ = "reStructuredText en"
__all__ = ["upload_subparser"]

import zeff
import zeff.record
from .utility import subparser_pipeline, build_pipeline


def upload_subparser(subparsers):
    """Add the ``upload`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the upload sub-command.
    """

    parser = subparsers.add_parser("upload")
    subparser_pipeline(parser)
    parser.add_argument(
        "--no-train",
        action="store_true",
        help="""Build, validate, and upload training records, but do not
            start training of machine.""",
    )
    parser.set_defaults(func=upload)


def upload(options):
    """Generate a set of records from options."""
    upload_success = build_pipeline(options, zeff.Uploader())
    if upload_success and not options.no_train:
        trainer = zeff.Trainer()
        trainer.start()
