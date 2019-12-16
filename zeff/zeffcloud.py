"""Zeff Cloud endpoints."""
__docformat__ = "reStructuredText en"

import re
import dataclasses
from typing import List, Dict
from pathlib import Path
import urllib.parse
import yaml


@dataclasses.dataclass
class ZeffCloudResource:
    """Defines how to access a specific resource.

    This contains the URL, method, required headers, allowed media
    types, and other information necessary to access a Zeff Cloud REST
    resources.

    :property tag_url: The URI tag scheme name for the resource.

    :property loc_url: The URL to the resource.

    :property methods: The HTTP methods that may be used on this.
    """

    # pylint: disable=too-few-public-methods

    tag_url: str
    loc_url: str
    methods: List[str]
    accept: List[str] = dataclasses.field(default_factory=list)
    headers: Dict[str, str] = dataclasses.field(default_factory=dict)

    def url(self, **argv):
        """Create a resolved URL.

        The ``loc_url`` may contain variables of the form ``{key}``. This
        will replace those with key-value pairs given as additional named
        arguments.

        :exception KeyError: If the ``loc_url`` has a variable and it
            is not in the named arguments.
        """
        return self.loc_url.format(**argv)

    def variables(self):
        """Return the list of variables in the URL.

        The ``loc_url`` may contain variables of the form ``{key}``. This
        will return the name of each of those variables.
        """
        return re.findall(r"{(\w+)}", self.loc_url)


class ZeffCloudResourceMap(dict):
    """Zeff Cloud map of tag URI to resources."""

    @classmethod
    def default_info(cls):
        """Return the default zeffcloud YAML configuration file."""

        dpath = Path(__file__).parent
        path = dpath / "zeffcloud.yml"
        with open(path, "r") as yfile:
            info = yaml.load(yfile, Loader=yaml.SafeLoader)
        return info

    def __init__(self, info, root="https://api.ziff.ai/", **argv):
        """Create mapping of tag URL to ZeffCloudResource objects.

        :param info: Mapping information.

        :param root: This is the root of the Zeff Cloud REST server. The
            default is the public location ``https://api.ziff.ai/``.

        :param **: Other arguments where the key the name used in a
            variable.
        """
        super().__init__()
        self.__root = root
        urlparts = list(urllib.parse.urlsplit(root))
        rootpath = urlparts[2]
        urlparts[3] = None
        urlparts[4] = None

        def_accept = info["accept"]
        def_headers = info["headers"]
        for c_res in info["links"]:
            urlparts[2] = f"{rootpath}/{c_res['anchor']}"
            urlparts[2] = urlparts[2].replace("//", "/")
            urlparts[2] = urlparts[2].lstrip("/")
            resource = ZeffCloudResource(
                c_res["tag"],
                urllib.parse.urlunsplit(urlparts),
                c_res["methods"],
                accept=c_res.get("accept", def_accept),
                headers={
                    key: value.format(**argv)
                    for key, value in c_res.get("headers", def_headers).items()
                },
            )
            super().__setitem__(resource.tag_url, resource)

    def __str__(self):
        """Return printable representation."""
        return f"<ZeffCloudResourceMap root={self.__root} mapping={super().__str__()}>"

    # def __repr__(self):
    # """Return offical string representation."""
    # pass
