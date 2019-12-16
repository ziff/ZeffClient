"""Zeff subcommand to train a machine."""
__docformat__ = "reStructuredText en"
__all__ = ["train_subparser"]

import sys
import errno
from time import sleep
from tqdm import tqdm
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud.dataset import Dataset
from zeff.cloud.training import TrainingStatus
from .server import subparser_server


def train_subparser(subparsers, config):
    """Add the ``train`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the train sub-command.
    """

    parser = subparsers.add_parser("train", help="""Control training sessions.""")
    parser.add_argument(
        "--records-datasetid",
        default=config.records.datasetid,
        help="""Dataset id to access for training.""",
    )
    subparser_server(parser, config)
    parser.set_defaults(func=train)

    actions = parser.add_subparsers(
        help="Send commands for training sessions on the specified dataset."
    )

    action_status = actions.add_parser(
        "status", help="Display status of current training session."
    )
    action_status.add_argument(
        "--continuous",
        default=False,
        action="store_true",
        help="Continuously display the status of the training session.",
    )
    action_status.set_defaults(action=Trainer.status)

    action_start = actions.add_parser(
        "start", help="Start or restart a training session."
    )
    action_start.set_defaults(action=Trainer.start)

    action_stop = actions.add_parser("stop", help="Stop the current training session.")
    action_stop.set_defaults(action=Trainer.stop)


def train(options):
    """Entry point for train subcommand."""
    if not options.records_datasetid:
        print("Unknown dataset id to access for training.", file=sys.stderr)
        sys.exit(errno.EINVAL)
    trainer = Trainer(options)
    options.action(trainer)


class Trainer:
    """Controller for dataset training."""

    def __init__(self, options):
        """Create new trainier controller."""
        self.options = options
        self.server_url = options.server_url
        self.org_id = options.org_id
        self.user_id = options.user_id
        self.dataset_id = options.records_datasetid

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=self.server_url, org_id=self.org_id, user_id=self.user_id
        )
        self.dataset = Dataset(self.dataset_id, self.resource_map)

    def status(self):
        """Print current status to stream."""

        def tstamp():
            return f"{tstate.updated_timestamp.strftime('%c')}"

        if self.options.continuous:

            def desc_str():
                return f"{tstate.status} ({tstamp()})"

            tstate = self.dataset.training_status
            pbar = tqdm(
                desc=desc_str(),
                total=100,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
            )
            while tstate.status is not TrainingStatus.complete:
                pbar.set_description(desc_str())
                pbar.update(tstate.progress)
                sleep(1.0)
                tstate = self.dataset.training_status
            pbar.close()
        else:
            tstate = self.dataset.training_status
            if tstate.status is TrainingStatus.queued:
                print(f"Queued as of {tstamp()}")
            elif tstate.status is TrainingStatus.started:
                print(f"Started on {tstamp()}")
            elif tstate.status is TrainingStatus.progress:
                print(f"Progress {tstate.progress:.2%} as of {tstamp()}")
            elif tstate.status is TrainingStatus.complete:
                print(f"Completed on {tstamp()}")

    def start(self):
        """Start or restart the current training session."""
        self.dataset.start_training()

    def stop(self):
        """Stop the current training session."""
        self.dataset.stop_training()
