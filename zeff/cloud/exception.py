"""Zeff Cloud Exceptions."""
__docformat__ = "reStructuredText en"

from typing import Type
import textwrap


class ZeffCloudException(Exception):
    """Base class for all exceptions when communicating with Zeff Cloud."""

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
            {self.__resource.__name__} {self.__resource_name} load failed
            with HTTP status {self.__resp.status_code} -
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


class ZeffCloudModelException(Exception):
    """Exceptions when working with a model."""

    def __init__(self, msg, model=None):
        """Create new exception.

        :param model: The model the problem occurred on or `None` if a
            model cannot be created.
        """
        super().__init__()
        self.__model = model
        self.__message = msg

    def __str__(self):
        """Return message string for exception."""
        if self.__model:
            ret = f"""\
                {self.__message}:
                model version {self.__model.version}
                dataset {self.__model.dataset_id}
                """
        else:
            ret = f"""{self.__message}"""
        return textwrap.dedent(ret).replace("\n", " ")
