"""Zeff commandline configuration."""
__docformat__ = "reStructuredText en"
__all__ = ["Configuration", "load_configuration"]


import sys
import errno
import dataclasses
import pathlib
import importlib
from configparser import ConfigParser, ExtendedInterpolation, ParsingError


@dataclasses.dataclass(init=False)
class Server:
    """Server configuration section."""

    server_url: str
    org_id: str
    user_id: str

    def __init__(self, config):
        self.server_url = config.get("server", "server_url")
        self.org_id = config.get("server", "org_id")
        self.user_id = config.get("server", "user_id")

    def update(self, options):
        """Update configuration from command line options."""
        self.server_url = getattr(options, "server_url", self.server_url)
        self.org_id = getattr(options, "org_id", self.org_id)
        self.user_id = getattr(options, "user_id", self.user_id)


@dataclasses.dataclass(init=False)
class Records:
    """Records configuration section."""

    datasetid: str
    records_config_generator: object
    records_config_arg: str
    record_builder: object
    record_builder_arg: str
    record_validator: object

    def __init__(self, config):
        self.datasetid = config.get("records", "datasetid")
        self.records_config_generator = get_mclass(
            config, "records", "records_config_generator"
        )
        self.records_config_arg = config.get("records", "records_config_arg")
        self.record_builder = get_mclass(config, "records", "record_builder")
        self.record_builder_arg = config.get("records", "record_builder_arg")
        self.record_validator = get_mclass(config, "records", "record_validator")

    def update(self, options):
        """Update configuration from command line options."""
        self.datasetid = getattr(options, "datasetid", self.datasetid)
        self.records_config_generator = getattr(
            options, "records_config_generator", self.records_config_generator
        )
        self.records_config_arg = getattr(
            options, "records_config_arg", self.records_config_arg
        )
        self.record_builder = getattr(options, "record_builder", self.record_builder)
        self.record_builder_arg = getattr(
            options, "record_builder_arg", self.record_builder_arg
        )
        self.record_validator = getattr(
            options, "record_validator", self.record_validator
        )


@dataclasses.dataclass(init=False)
class Configuration:
    """CLI configuration.

    This loads from the ``zeff.conf`` configuration file and converts to
    typed objects for ease of use.

    :property server_url: The Zeff Cloud REST server URL.

    :property org_id: Organization ID for use in authentication.

    :property user_id: User ID  for use in authentication.

    :property datasetid: Dataset that defines where records should be uplaoded.

    :property records_config_generator: Class to construct the generator
        for building configuration values to be sent to the record builder.

    :property records_config_arg: Single argument to be given to the
        ``records_config_generator`` when created.

    :property record_builder: Class to construct the record builder.

    :property record_builder_arg: Single argument to be given to the
        ``record_builder`` when created.

    :property record_validator: Class to construct a record validator.
    """

    server: Server
    records: Records

    def __init__(self, config):
        """Create a configuration object from a ConfigParser object."""
        self.server = Server(config)
        self.records = Records(config)

    def update(self, options):
        """Update configuration from command line options."""
        self.server.update(options)
        self.records.update(options)


def load_configuration() -> Configuration:
    """Load configuration from standard locations.

    Configuration files will be loaded in the following order such that
    values in later files will override those in earlier files:

        1. ``/etc/zeff.conf``
        2. ``${HOME}/.config/zeff/zeff.conf``
        3. ``${PWD}/zeff.conf``

    Variable substitution is available where a variable is of the form
    ``${section:option}``. If section is omitted then the current section
    will be used and then from the default section. In the default
    section there are some pre-defined values:

        ``${HOME}``
            Home directory of the user.

        ``${PWD}``
            The current working directory the application was started in.
    """

    config = ConfigParser(
        strict=True,
        allow_no_value=False,
        delimiters=["="],
        comment_prefixes=["#"],
        interpolation=ExtendedInterpolation(),
        defaults={"HOME": str(pathlib.Path.home()), "PWD": str(pathlib.Path.cwd())},
    )
    try:
        config.read(
            [
                pathlib.Path(__file__).parent / "configuration_default.conf",
                pathlib.Path("/etc/zeff.conf"),
                pathlib.Path.home() / ".config" / "zeff" / "zeff.conf",
                pathlib.Path.cwd() / "zeff.conf",
            ]
        )
    except ParsingError as err:
        sys.exit(err)

    return Configuration(config)


def get_mclass(config, section, option):
    """Return class object for given option."""

    path = config.get(section, option)
    if not path:
        return None
    if isinstance(path, type):
        return path
    # logging.debug("Look for `%s`", path)
    try:
        m_name, c_name = path.rsplit(".", 1)
        module = importlib.import_module(m_name)
        # logging.debug("Found module `%s`", m_name)
        return getattr(module, c_name)
    except ValueError:
        print(
            f"Required value for [{section}]{option} missing or incorrect format: ``{path}``.",
            file=sys.stderr,
        )
        sys.exit(errno.EINVAL)
    except ModuleNotFoundError:
        print(
            f"[{section}]{option} module `{m_name}` not found in PYTHONPATH={sys.path}",
            file=sys.stderr,
        )
        sys.exit(errno.EINVAL)
    except AttributeError:
        print(
            f"[{section}]{option} class `{c_name}` not found in {m_name}",
            file=sys.stderr,
        )
        sys.exit(errno.EINVAL)
