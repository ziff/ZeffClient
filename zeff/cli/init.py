"""Zeff subcommand to initialize a new project."""
__docformat__ = "reStructuredText en"
__all__ = ["init_subparser"]

import sys
import errno
import argparse
from string import Template
from pathlib import Path, PurePath
import importlib
from zeff.zeffdatasettype import ZeffDatasetType
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud import Dataset, ZeffCloudException

CONF_PATH = Path.cwd() / "zeff.conf"


def init_subparser(subparsers):
    """Add the ``init`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the init sub-command.
    """
    parser = subparsers.add_parser(
        "init", help="""Setup a new project in the current directory."""
    )
    parser.add_argument(
        "dataset_type",
        choices=[e.name for e in ZeffDatasetType],
        action=DatasetTypeAction,
        help="""Type of project to create.""",
    )
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="""If source files exist overwrite with template.""",
    )
    parser.set_defaults(func=init_project)


class DatasetTypeAction(argparse.Action):
    """Convert a dataset type string into associated enum."""

    # pylint: disable=too-few-public-methods

    def __call__(self, parser, namespace, values, option_string=None):
        values = getattr(ZeffDatasetType, values)
        setattr(namespace, self.dest, values)


def init_project(options):
    """Initialize a new project in the current directory."""
    try:
        Project(options)()
    except ValueError as err:
        print("ERROR:", err, file=sys.stderr)
        sys.exit(1)
    except ZeffCloudException as err:
        print("ERROR:", err, file=sys.stderr)
        sys.exit(errno.EIO)


class Project:
    """Create a new project."""

    def __init__(self, options):
        self.options = options
        self.config = self.options.configuration
        self.record_validator = self.options.dataset_type.validator

    def __call__(self):
        self.create_zeff_conf()
        self.create_generator()
        self.create_builder()
        with open(CONF_PATH, "wt") as fout:
            self.config.write(fout)

        self.create_dataset()
        with open(CONF_PATH, "wt") as fout:
            self.config.write(fout)

    def create_zeff_conf(self):
        """Ask user for configuration options and create `zeff.conf`.

        This will create or update the zeff.conf file and will update the
        configuration that is in options for use in other init operations.
        """

        defaults = {"HOME": str(Path.home()), "PWD": str(Path.cwd())}

        def ask_update(section_name, option_name, msg, use_variables=False):
            section = getattr(self.config, section_name)
            value = getattr(section, option_name, "")
            if isinstance(value, type):
                value = f"{value.__module__}.{value.__name__}"
            elif callable(value):
                value = f"{value.__module__}.{value.__name__}"
            else:
                value = str(value)
            prompt = f"{msg} [{value}]? "
            resp = input(prompt)
            if resp and resp != value:
                value = resp
                if use_variables:
                    for defk, defv in defaults.items():
                        scratch = resp.replace(defv, f"${{{defk.upper()}}}")
                        if len(scratch) < len(value):
                            value = scratch
                setattr(section, option_name, value)
            return value

        # Server
        ask_update("server", "server_url", "Server URL")
        ask_update("server", "org_id", "Organization ID")
        ask_update("server", "user_id", "User ID")

        # Records
        ask_update("records", "dataset_title", "Dataset Title")
        ask_update("records", "dataset_desc", "Dataset Description")

        ask_update(
            "records", "records_config_generator", "Configuration generator python name"
        )
        ask_update(
            "records",
            "records_config_arg",
            "Configuration generator init argument",
            use_variables=True,
        )
        ask_update("records", "record_builder", "Record builder python name")
        ask_update(
            "records",
            "record_builder_arg",
            "Record builder init argument",
            use_variables=True,
        )

        ask_update(
            "records",
            "record_validator",
            "Record validator python name",
            use_variables=True,
        )

        self.config.validate()
        print()

    def create_dataset(self):
        """Create dataset on server and update config file."""
        if self.options.configuration.records.datasetid == "":
            datasettype = self.options.dataset_type
            dataset_title = self.config.records.dataset_title
            if not dataset_title:
                raise ValueError("Creation of a dataset requires a title.")
            dataset_desc = self.config.records.dataset_desc
            if not dataset_desc:
                raise ValueError("Creation of a dataset requires a description.")
            resource_map = ZeffCloudResourceMap(
                ZeffCloudResourceMap.default_info(),
                root=self.config.server.server_url,
                org_id=self.config.server.org_id,
                user_id=self.config.server.user_id,
            )
            dataset = Dataset.create_dataset(
                resource_map, datasettype, dataset_title, dataset_desc
            )
            self.config.records.datasetid = dataset.dataset_id

    def create_generator(self):
        """Create record generator template code."""
        self.create_python_from_template(
            self.config.records.records_config_generator,
            "RecordGenerator",
            "RecordGenerator.template",
        )

    def create_builder(self):
        """Create record builder template code."""
        self.create_python_from_template(
            self.config.records.record_builder,
            "RecordBuilder",
            "RecordBuilder.template",
        )

    def create_python_from_template(self, obj, name_ext, template_name):
        """Create a source file from a template.

        :param obj: This is either the name of the type or callable to
            be created, or is the type or callable to be created.

        :param name_ext: String in template file to replace with name of
            `obj`.

        :param template_name: Name of template file.
        """
        if isinstance(obj, str):
            m_name, c_name = obj.rsplit(".", 1)
        else:
            m_name = obj.__module__
            c_name = obj.__name__
        try:
            module = importlib.import_module(m_name)
            getattr(module, c_name)
            print(f"Skipping creation of {m_name}.{c_name} it exists in PYTHONPATH.")
            return
        except ModuleNotFoundError:
            pass
        except AttributeError:
            pass

        name = c_name.replace(name_ext, "")
        if name == "":
            name = Path.cwd().name

        template_path = PurePath(__file__).parent.joinpath(template_name)
        with open(template_path, "rt") as template_file:
            template = Template(template_file.read())

        output_path = Path.cwd() / f"{m_name}.py"
        if output_path.exists() and not self.options.overwrite_existing:
            print(f"Skipping creation of {m_name}.py as it already exists.")
        else:
            with open(output_path, "wt") as fout:
                fout.write(template.safe_substitute(name=name, c_name=c_name))
            output_path.chmod(0o755)
