"""Zeff Cloud Exceptions."""
__docformat__ = "reStructuredText en"

from typing import Type
import textwrap


class ZeffCloudException(Exception):
    """Base class for all exceptions when working with Zeff Cloud."""

    def __init__(self, resp, resource: Type, resource_name: str, action: str):
        """Create new exception.

        :param resp: HTTP response object of request that failed.

        :param resource: Type of Zeff Cloud resource being accessed.

        :param resource_name: Name or id of Zeff Cloud resource being accessed.

        :param action: Name of action that was being performed.
        """
        super().__init__()
        self.__resp = resp
        self.__resource = resource
        self.__resource_name = resource_name
        self.__action = action

    def __str__(self):
        """Return message string for exception."""
        return textwrap.dedent(
            f"""\
            {self.__resource} {self.__resource_name} load failed {self.__resp.status_code} -
            {self.__resp.reason}: {self.__resp.text}
            """
        ).replace("\n", " ")

    @property
    def response(self):
        """Return response object from HTTP request that caused this exception."""
        return self.__resp

    @property
    def resource(self):
        """Return resource type involved with the request."""
        return self.__resource

    @property
    def resource_name(self):
        """Return resource name or id for the request."""
        return self.__resource_name

    @property
    def action(self):
        """Return action that was attempted."""
        return self.__action
