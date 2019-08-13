#!/usr/bin/env python3
"""Zeff record builder for HousePrice records."""
__version__ = "0.0"

import logging
import pathlib
import urllib.parse
import csv
from zeff.record import *

LOGGER = logging.getLogger("zeffclient.record.builder")


class HousePriceRecordBuilder:
    """Record builder for HousePrice records.

    The callable object has a single `config` parameter that the record
    builder understands. This could be a URL, a unique number that is
    a primary key in the database, or a full configuration file.
    """

    def __init__(self, arg: str):
        pass

    def __call__(self, config: str) -> Record:
        urlparts = urllib.parse.urlsplit(config)
        path = pathlib.Path(urlparts[2])
        id = urlparts[3].split("=")[1]
        LOGGER.info("Begin building ``HousePrice`` record from %s", id)
        record = Record(name=id)
        self.add_structured_data(record, path, id)
        self.add_unstructured_data(record, path.parent, id)
        LOGGER.info("End building ``HousePrice`` record from %s", id)
        return record

    def add_structured_data(self, record, path, id):
        row = None
        with open(path, "r") as csvfile:
            row = [r for r in csv.DictReader(csvfile) if r["id"] == id]
            if len(row) == 0:
                return
            row = row[0]

        # Process each field in the record except for `id` and
        # add it as a structured data to the record object.
        for key in row.keys():
            if key == "id":
                continue
            value = row[key]

            # Is the column a continuous or category datatype
            if isinstance(value, (int, float)):
                dtype = StructuredData.DataType.CONTINUOUS
            else:
                dtype = StructuredData.DataType.CATEGORY

            # Create the structured data item and add it to the
            # structured data object
            sd = StructuredData(name=key, value=value, data_type=dtype)
            sd.record = record

    def add_unstructured_data(self, record, path, id):

        img_path = path / f"images_{id}"

        # Process each jpeg file in the image path, create an
        # unstructured data, and add it to the record object.
        for p in img_path.glob("**/*.jpeg"):
            url = f"file://{p}"
            file_type = UnstructuredData.FileType.IMAGE
            group_by = "home_photo"
            ud = UnstructuredData(url, file_type, group_by=group_by)
            ud.record = record


if __name__ == "__main__":
    import sys
    from logging import basicConfig, DEBUG
    import errno
    import argparse
    from pathlib import Path
    from zeff.cli import load_configuration
    from zeff.record import format_record_restructuredtext

    if sys.version_info < (3, 7):
        raise Exception("{0} requires Python 3.7.".format(sys.argv[0]))

    basicConfig(level=DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("config", help="Configuration to build HousePrice record")
    options = parser.parse_args()
    config = load_configuration()

    try:
        builderarg = config["records"]["record_builder_arg"]
        builder = HousePriceRecordBuilder(builderarg)
        record = builder(options.config)
        record.validate()
        format_record_restructuredtext(record, out=sys.stdout)
    except TypeError as err:
        logging.error(f"Record Validation Failed {err}")
        sys.exit(1)
    except ValueError as err:
        logging.error(f"Record Validation Failed {err}")
        sys.exit(1)
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
