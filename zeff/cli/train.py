"""Zeff subcommand to train a machine."""
__docformat__ = "reStructuredText en"
__all__ = ["train_subparser"]

import zeff
import zeff.record


def train_subparser(subparsers):
    """Add the ``train`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the train sub-command.
    """

    parser = subparsers.add_parser("train")
    parser.add_argument(
        "action",
        choices=["start", "stop", "kill"],
        help="""Proform the given action on Zeff Cloud:
            start - start training the current session,
            stop - stop training the current session,
            kill - kill current session and mark as invalid""",
    )
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
