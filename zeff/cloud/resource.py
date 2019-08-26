"""Zeff Cloud REST resource."""
__docformat__ = "reStructuredText en"

import logging
import re
import json
import importlib
import requests
from .exception import ZeffCloudException

LOGGER = logging.getLogger("zeffclient.record.uploader")


class Resource:
    """Base class for accessing Zeff Cloud REST resources."""

    # pylint: disable=too-few-public-methods

    @classmethod
    def snake_case(cls, name):
        """Convert camel case `name` to snake case."""
        name = re.sub(r"([A-Z])", r"_\1", name).lstrip("_")
        name = name.lower()
        return name

    def __init__(self, resource_map):
        """Link object to REST resource.

        :param resource_map: Map of URI tag names to ZeffCloudResource
            objects.
        """
        self.resource_map = resource_map

    def request(self, tag, method="GET", data=None, headers=None, **kwargs):
        """Send request to Zeff Cloud server and return response.

        :param tag: Tag that identifies anchor and methods.

        :param data: Data to send in request.

        :param headers: Additional headers to send with request.

        :param **: Arguments to use in creating the URL. The key should
            match the variable in the anchor.

        :return: The response from the server.

        Default Headers:

            - Accept
            - Content-Type
            - Content-Length
            - x-api-key
        """
        res = self.resource_map[tag]
        assert method in res.methods, f"Invalid method `{method}` for `{tag}`."

        url = res.url(**kwargs)

        reqhdrs = dict(res.headers)
        reqhdrs["Accept"] = "application/json"
        if method in ["POST", "PUT"]:
            reqhdrs["Content-Type"] = "application/json"
        if headers:
            reqhdrs.update(headers)

        resp = requests.request(method, url, data=data, headers=reqhdrs)
        return resp

    def add_resource(self, rsrc, rsrc_name, rsrc_id_name, tag, **kwargs):
        """Add a resource to this resource.

        This generalizes the operation of adding to a set of resources
        contained by this resource.

        .. warn::
            There must be a class in ``encoder.py`` that has the name
            ``{rsrc.__name__}Encoder`` for this method to operate correctly.

        :param rsrc: The resource to be added.

        :param rsrc_name: The unique name to be used for the resource.

        :param rsrc_id_name: The id key name in the returned data.

        :param tag: The tag in the resource map that identifies the URL.

        :param args: TBD

        :param kwargs: Additional keyword arguments that match named
            variables in the tagged URL. This list should not included
            variables that name properties of this resource as those
            will be looked up.
        """
        rsrc_type = type(rsrc).__name__
        LOGGER.info("Begin upload %s %s", rsrc_type, rsrc_name)

        res = self.resource_map[tag]
        res_vars = {
            k: getattr(self, k)
            for k in (v for v in res.variables() if v not in kwargs.keys())
        }
        encoder = getattr(
            importlib.import_module(".encoder", package=__package__),
            f"{rsrc_type}Encoder",
        )
        batch = {"batch": [rsrc]}
        resp = self.request(
            tag,
            method="POST",
            data=json.dumps(batch, cls=encoder),
            **res_vars,
            **kwargs,
        )
        if resp.status_code not in [200, 201]:
            raise ZeffCloudException(
                resp, type(self), rsrc_name, f"add {rsrc.__name__}"
            )
        data = resp.json()["data"][0]
        LOGGER.info(
            """End upload %s %s: recordId = %s location = %s""",
            rsrc_type,
            rsrc_name,
            data.get(rsrc_id_name, "unknown"),
            data.get("location", "unknown"),
        )
        return data
