"""Zeff subcommand to initialize a new project."""
__docformat__ = "reStructuredText en"
__all__ = ["init_subparser"]

import sys
import errno
from string import Template
from pathlib import Path, PurePath
import importlib
from configparser import ConfigParser, ExtendedInterpolation, NoOptionError
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
        "--overwrite-existing",
        action="store_true",
        help="""If source files exist overwrite with template.""",
    )
    parser.set_defaults(func=init_project)


def init_project(options):
    """Initialize a new project in the current directory."""
    try:
        Project(options)()
    except ZeffCloudException as err:
        print(err, file=sys.stderr)
        sys.exit(errno.EIO)


class Project:
    """Create a new project."""

    def __init__(self, options):
        self.options = options
        self.optconf = self.options.configuration
        self.config = ConfigParser(
            strict=True,
            allow_no_value=False,
            delimiters=["="],
            comment_prefixes=["#"],
            interpolation=ExtendedInterpolation(),
        )
        self.config.read(CONF_PATH)
        for section in (
            s for s in self.optconf.sections() if s not in self.config.sections()
        ):
            self.config.add_section(section)

    def __call__(self):
        self.create_zeff_conf()
        self.create_dataset()
        self.create_generator()
        self.create_builder()

        with open(CONF_PATH, "wt") as fout:
            self.config.write(fout)

        for defk, defv in self.optconf.defaults().items():
            self.config.set("DEFAULT", defk, defv)

        self.optconf.read_dict(self.config)

    def create_zeff_conf(self):
        """Ask user for configuration options and create `zeff.conf`.

        This will create or update the zeff.conf file and will update the
        configuration that is in options for use in other init operations.
        """

        def ask_update(section, option, msg, use_variables=False):
            value = self.optconf.get(section, option, fallback="")
            prompt = f"{msg} [{value}]? "
            resp = input(prompt)
            if resp and resp != value:
                value = resp
                if use_variables:
                    for defk, defv in self.optconf.defaults().items():
                        scratch = resp.replace(defv, f"${{{defk.upper()}}}")
                        if len(scratch) < len(value):
                            value = scratch
                self.config.set(section, option, value)
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

    def create_dataset(self):
        """Create dataset on server and update config file."""
        if self.options.configuration.get("records", "datasetid") == "":
            try:
                dataset_title = self.config.get("records", "dataset_title")
                dataset_desc = self.config.get("records", "dataset_desc")
            except NoOptionError:
                return
            resource_map = ZeffCloudResourceMap(
                ZeffCloudResourceMap.default_info(),
                root=self.optconf.get("server", "server_url"),
                org_id=self.optconf.get("server", "org_id"),
                user_id=self.optconf.get("server", "user_id"),
            )
            dataset = Dataset.create_dataset(resource_map, dataset_title, dataset_desc)
            datasetid = dataset.dataset_id
            self.config.set("records", "datasetid", datasetid)

    def create_generator(self):
        """Create record generator template code."""
        self.create_python_from_template(
            "records_config_generator", "RecordGenerator", "RecordGenerator.template"
        )

    def create_builder(self):
        """Create record builder template code."""
        self.create_python_from_template(
            "record_builder", "RecordBuilder", "RecordBuilder.template"
        )

    def create_python_from_template(self, option, name_ext, template_name):
        """Create a source file from a template."""
        path = self.config["records"][option]
        m_name, c_name = path.rsplit(".", 1)
        try:
            module = importlib.import_module(m_name)
            getattr(module, c_name)
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
