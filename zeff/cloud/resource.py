"""Zeff Cloud REST resource."""
__docformat__ = "reStructuredText en"

import logging
import requests

LOGGER = logging.getLogger("zeffclient.record.uploader")


class Resource:
    """Base class for accessing Zeff Cloud REST resources."""

    # pylint: disable=too-few-public-methods

    def __init__(self, resource_map):
        """Link object to REST resource.

        :param resource_map: Map of URI tag names to ZeffCloudResource
            objects.
        """
        self.resource_map = resource_map

    def request(self, tag, method="GET", data=None, headers=None, **argv):
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

        url = res.url(**argv)

        reqhdrs = dict(res.headers)
        reqhdrs["Accept"] = "application/json"
        if method in ["POST", "PUT"]:
            reqhdrs["Content-Type"] = "application/json"
        if headers:
            reqhdrs.update(headers)

        resp = requests.request(method, url, data=data, headers=reqhdrs)
        return resp
