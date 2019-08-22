"""Zeff subcommand to train a machine."""
__docformat__ = "reStructuredText en"
__all__ = ["train_subparser"]

import sys
import errno
import zeff
from .server import subparser_server
import zeff.record
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud.exception import ZeffCloudException
from zeff.cloud.dataset import Dataset, TrainingSessionInfo


def train_subparser(subparsers, config):
    """Add the ``train`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the train sub-command.
    """

    parser = subparsers.add_parser("train", help="""Control training sessions.""")
    parser.add_argument(
        "--records-datasetid",
        default=config["records"]["datasetid"],
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

    action_kill = actions.add_parser("kill", help="Kill the current training session.")
    action_kill.set_defaults(action=Trainer.kill)


def train(options):
    """Generate a set of records from options."""
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
        from tqdm import tqdm
        import time

        if self.options.continuous:
            s = self.dataset.training_status
            pbar = tqdm(
                desc=str(s.status),
                total=100,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
            )
            while s.status is not TrainingSessionInfo.Status.complete:
                pbar.set_description(str(s.status))
                pbar.update(s.progress)
                time.sleep(1.0)
                s = self.dataset.training_status
            pbar.close()
        else:
            s = self.dataset.training_status
            if s.status is TrainingSessionInfo.Status.queued:
                print(f"Queued as of {s.updated_timestamp.strftime('%c')}")
            elif s.status is TrainingSessionInfo.Status.started:
                print(f"Started on {s.updated_timestamp.strftime('%c')}")
            elif s.status is TrainingSessionInfo.Status.progress:
                print(
                    f"Progress {s.progress:.2%} as of {s.updated_timestamp.strftime('%c')}"
                )
            elif s.status is TrainingSessionInfo.Status.complete:
                print(f"Completed on {s.updated_timestamp.strftime('%c')}")

    def start(self):
        """Start or restart the current training session."""
        self.dataset.start_training()

    def stop(self):
        """Stop the current training session."""
        self.dataset.stop_training()

    def kill(self):
        """Kill the current training session and mark invalid."""
        self.dataset.kill_training()
