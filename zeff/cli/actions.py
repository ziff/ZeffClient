"""Zeff commandline argparse custom actions."""
__docformat__ = "reStructuredText en"

import argparse
import importlib


class NamedClassObjectAction(argparse.Action):
    """Converts a string into a python class object if it exists."""

    # pylint: disable=too-few-public-methods

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """See argparse.Action."""

        if "default" in kwargs and isinstance(kwargs["default"], type):
            clazz = kwargs["default"]
            path = ".".join([clazz.__module__, clazz.__name__])
            kwargs["help"] = kwargs["help"].replace("%(default)s", path)
        else:
            kwargs["help"] = kwargs["help"].replace("%(default)s", "")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parse, namespace, values, option_string=None):
        """See argparse.Action."""

        try:
            m_name, c_name = values.rsplit(".", 1)
            module = importlib.import_module(m_name)
            obj = getattr(module, c_name)
            if not isinstance(obj, (type)):
                raise TypeError(
                    f"``{values}`` must a class object not ``{type(obj)}``."
                )
            setattr(namespace, self.dest, obj)
        except ValueError:
            raise ValueError(f"Argument ``{values}`` is not in class path format.")


class NamedCallableObjectAction(argparse.Action):
    """Converts a string into a python callable object if it exists."""

    # pylint: disable=too-few-public-methods

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """See argparse.Action."""

        if "default" in kwargs and isinstance(kwargs["default"], type):
            clazz = kwargs["default"]
            path = ".".join([clazz.__module__, clazz.__name__])
            kwargs["help"] = kwargs["help"].replace("%(default)s", path)
        else:
            kwargs["help"] = kwargs["help"].replace("%(default)s", "")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parse, namespace, values, option_string=None):
        """See argparse.Action."""

        try:
            m_name, c_name = values.rsplit(".", 1)
            module = importlib.import_module(m_name)
            obj = getattr(module, c_name)
            if not callable(obj):
                raise TypeError(
                    f"``{values}`` must a callable object not ``{type(obj)}``."
                )
            setattr(namespace, self.dest, obj)
        except ValueError:
            raise ValueError(f"Argument ``{values}`` is not in class path format.")
