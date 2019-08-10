"""Zeff subcommand to initialize a new project."""
__docformat__ = "reStructuredText en"
__all__ = ["init_subparser"]

from string import Template
from pathlib import Path, PurePath
import importlib
from configparser import ConfigParser, ExtendedInterpolation, NoOptionError

CONF_PATH = Path.cwd() / "zeff.conf"


def init_subparser(subparsers):
    """Add the ``init`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the init sub-command.
    """
    parser = subparsers.add_parser(
        "init", help="""Setup a new project in the current directory."""
    )
    parser.set_defaults(func=init_project)


def init_project(options):
    """Initialize a new project in the current directory."""

    create_zeff_conf(options)
    create_dataset(options)
    create_generator(options)
    create_builder(options)


def create_zeff_conf(options):
    """Ask user for configuration options and create `zeff.conf`.

    This will create or update the zeff.conf file and will update the
    configuration that is in options for use in other init operations.
    """
    optconf = options.configuration
    config = ConfigParser(
        strict=True,
        allow_no_value=False,
        delimiters=["="],
        comment_prefixes=["#"],
        interpolation=ExtendedInterpolation(),
    )
    config.read(CONF_PATH)
    for section in (s for s in optconf.sections() if s not in config.sections()):
        config.add_section(section)

    def ask_update(section, option, msg, use_variables=False):
        value = optconf.get(section, option, fallback="")
        prompt = f"{msg} [{value}]? "
        resp = input(prompt)
        if resp and resp != value:
            value = resp
            if use_variables:
                for defk, defv in optconf.defaults().items():
                    scratch = resp.replace(defv, f"${{{defk.upper()}}}")
                    if len(scratch) < len(value):
                        value = scratch
            config.set(section, option, value)
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

    with open(CONF_PATH, "wt") as fout:
        config.write(fout)

    for defk, defv in optconf.defaults().items():
        config.set("DEFAULT", defk, defv)

    optconf.read_dict(config)


def create_dataset(options):
    """Create dataset on server and update config file."""
    if options.configuration.get("records", "datasetid") == "":
        config = ConfigParser(
            strict=True,
            allow_no_value=False,
            delimiters=["="],
            comment_prefixes=["#"],
            interpolation=ExtendedInterpolation(),
        )
        config.read(CONF_PATH)

        try:
            dataset_title = config.get("records", "dataset_title")
            dataset_desc = config.get("records", "dataset_desc")
        except NoOptionError:
            return

        # Create the dataset when code is available
        datasetid = f"{dataset_title}#{dataset_desc}"

        config.set("records", "datasetid", datasetid)
        with open(CONF_PATH, "wt") as fout:
            config.write(fout)


def create_generator(options):
    """Create record generator template code."""
    path = options.configuration["records"]["records_config_generator"]
    create_python_from_template(path, "RecordGenerator", "RecordGenerator.template")


def create_builder(options):
    """Create record builder template code."""
    path = options.configuration["records"]["record_builder"]
    create_python_from_template(path, "RecordBuilder", "RecordBuilder.template")


def create_python_from_template(path, name_ext, template_name):
    """Create a source file from a template."""
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
    with open(output_path, "wt") as fout:
        fout.write(template.safe_substitute(name=name, c_name=c_name))
