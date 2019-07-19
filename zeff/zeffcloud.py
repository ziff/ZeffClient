"""Zeff Cloud endpoints."""
__docformat__ = "reStructuredText en"

import dataclasses
from typing import List, Dict
import urllib.parse
import yaml
from deprecated import deprecated


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


class ZeffCloudResourceMap(dict):
    """Zeff Cloud map of tag URI to resources."""

    @classmethod
    @deprecated(version="0.0.0", reason="For initial testing only.")
    def default_instance(cls):
        """Get the default instance of the mapping."""
        config = {"org_id": "example.com", "user_id": "kilroy"}
        if not hasattr(cls, "_ZeffCloudResourceMap__default_instance"):
            from pathlib import Path

            dpath = Path(__file__).parent
            path = dpath / "zeffcloud.yml"
            with open(path, "r") as yfile:
                cls.__default_instance = ZeffCloudResourceMap(yfile, config)
        return cls.__default_instance

    def __init__(self, stream, config, root="https://api.ziff.ai/"):
        """Create mapping of tag URL to ZeffCloudResource objects.

        :param stream: Stream that contains the resource mapping.

        :param config: Configuration object that contains specific items
            such as ``org_id`` or ``user_id``.

        :param root: This is the root of the Zeff Cloud REST server. The
            default is the public location ``https://api.ziff.ai/``.
        """
        super().__init__()
        self.__root = root
        urlparts = list(urllib.parse.urlsplit(root))
        rootpath = urlparts[2]
        urlparts[3] = None
        urlparts[4] = None

        info = yaml.load(stream, Loader=yaml.SafeLoader)
        def_accept = info["accept"]
        def_headers = info["headers"]
        for c_res in info["resources"]:
            urlparts[2] = f"{rootpath}/{c_res['path']}"
            urlparts[2] = urlparts[2].replace("//", "/")
            urlparts[2] = urlparts[2].lstrip("/")
            resource = ZeffCloudResource(
                c_res["tag"],
                urllib.parse.urlunsplit(urlparts),
                c_res["methods"],
                accept=c_res.get("accept", def_accept),
                headers={
                    key: value.format(**config)
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
