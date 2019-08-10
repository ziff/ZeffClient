"""Zeff subcommand to train a machine."""
__docformat__ = "reStructuredText en"
__all__ = ["train_subparser"]

import zeff
import zeff.record
from .server import subparser_server


def train_subparser(subparsers, config):
    """Add the ``train`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the train sub-command.
    """

    parser = subparsers.add_parser("train", help="""Control training sessions.""")
    parser.add_argument(
        "action",
        choices=["start", "stop", "kill"],
        help="""Perform the given action on Zeff Cloud:
            start - start training the current session,
            stop - stop training the current session,
            kill - kill current session and mark as invalid""",
    )
    subparser_server(parser, config)
    parser.set_defaults(func=train)


def train(options):
    """Generate a set of records from options."""
    trainer = zeff.Trainer()
    if options.action == "start":
        trainer.start()
    elif options.action == "stop":
        trainer.stop()
    elif options.action == "kill":
        trainer.kill()
