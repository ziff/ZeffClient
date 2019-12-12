"""Zeff subcommand to manage dataset models."""
__docformat__ = "reStructuredText en"
__all__ = ["models_subparser"]

import sys
import errno
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud.dataset import Dataset
from .server import subparser_server


def models_subparser(subparsers, config):
    """Add the ``models`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the models sub-command.
    """

    parser = subparsers.add_parser("models", help="""Manage dataset models.""")
    parser.add_argument(
        "--records-datasetid",
        default=config.records.datasetid,
        help="""Dataset id for set of models to manage.""",
    )
    subparser_server(parser, config)
    parser.set_defaults(func=models)

    actions = parser.add_subparsers(help="Commands to manage models.")

    action_list = actions.add_parser("list", help="List all models in the dataset.")
    action_list.set_defaults(action=Models.list)


def models(options):
    """Entry point for models subcommand."""
    if not options.records_datasetid:
        print("Unknown dataset id for managing models.", file=sys.stderr)
        sys.exit(errno.EINVAL)
    controller = Models(options)
    options.action(controller)


class Models:
    """Controller for dataset models management."""

    # pylint: disable=too-few-public-methods

    def __init__(self, options):
        """Create new models manager."""
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

    def list(self):
        """List all models in the dataset."""
        for model in self.dataset.models():
            print(
                f"{model.version:3d} {model.status} {model.updated_timestamp.strftime('%c')}"
            )
