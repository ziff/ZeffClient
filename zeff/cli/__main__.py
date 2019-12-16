#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------
"""zeff is a CLI tool that simplifies experimentation with Zeff Cloud API."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"

import sys

if sys.version_info < (3, 7):
    raise Exception("{0} Requires Python 3.7 or higher.".format(sys.argv[0]))


def main(args=None):
    """Configure system from command line arguments and configuration files."""
    # pylint: disable=broad-except
    # pylint: disable=import-outside-toplevel

    import traceback
    import errno
    import pathlib
    import logging
    import zeff.cli

    zeff.cli.configure_logging()

    cwd = str(pathlib.Path.cwd())
    if cwd not in sys.path:
        sys.path.append(cwd)
    options = zeff.cli.parse_commandline(args=args)

    try:
        logging.info("Starting with options %s", options)
        options.func(options)
    except SystemExit as err:
        logging.info("System exit")
        raise
    except InterruptedError as err:
        logging.info("Interrupt")
    except KeyboardInterrupt as err:
        logging.debug("Keyboard interrupt")
        sys.exit(errno.EINTR)
    except Exception as err:
        logging.exception("Unhandled exception.")
        sys.exit(1)


if __name__ == "__main__":
    main()
