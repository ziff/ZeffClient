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
    import traceback
    import errno
    import logging
    import zeff.cli

    options = zeff.cli.parse_commandline(args=args)

    try:
        import ast
        from logging import config

        with open(options.logging_conf, "r") as file:
            log_dict = ast.literal_eval(file.read())
            config.dictConfig(log_dict)
        logging.getLogger().setLevel(options.verbose.upper())
    except Exception as err:
        if options.verbose == "debug":
            traceback.print_exception(
                err.__class__, err, err.__traceback__, file=sys.stderr
            )
        else:
            print(
                "Unhandled exception while configuring logging:", err, file=sys.stderr
            )
        sys.exit(1)

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
