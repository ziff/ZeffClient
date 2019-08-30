"""Zeff subcommand to use machine to make a prediction."""
__docformat__ = "reStructuredText en"
__all__ = ["predict_subparser"]

import sys
from pathlib import Path
from time import sleep
import datetime
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
        type=int,
        help="""Choose a model version to make prediction against. The
            default is the latest valid version.""",
    )
    subparser_pipeline(parser, config)
    parser.set_defaults(func=predict)


def predict(options):
    """Generate a set of records from options."""
    sys.path.append(str(Path.cwd()))
    now = datetime.datetime.utcnow()
    try:
        _, records = build_pipeline(options, zeff.Predictor, options.model_version)
    except zeff.cloud.exception.ZeffCloudModelException as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    records = list(records)
    backoff = 1.0
    cutoff = 64.0
    while backoff < cutoff and records:
        sleep(backoff)
        backoff = backoff * 2
        for record in list(records):
            if record.updated_timestamp > now:
                records.remove(record)
                print(record)
    for record in records:
        print(
            "Predictions not complete {record.record_id} in dataset {record.dataset_id}"
        )
