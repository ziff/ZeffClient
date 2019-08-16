"""Zeff subcommand to use machine to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["predict_subparser"]

import sys
from pathlib import Path
import logging
import zeff
import zeff.record
from .pipeline import subparser_pipeline, build_pipeline


def predict_subparser(subparsers, config):
    """Add the ``predict`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the predict sub-command.
    """

    parser = subparsers.add_parser(
        "predict", help="""Upload record to infer a prediction."""
    )
    parser.add_argument(
        "--model-version",
        dest="model-version",
        help="""Choose a model version to make prediction against. The
            default is the latest valid version.""",
    )
    subparser_pipeline(parser, config)
    parser.set_defaults(func=predict)


def predict(options):
    """Generate a set of records from options."""
    sys.path.append(str(Path.cwd()))
    _, records = build_pipeline(options, zeff.Predictor)
    for record in records:
        logging.debug(record)
    # Get the results and output them
