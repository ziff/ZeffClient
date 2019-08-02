#!/usr/bin/env python3
"""Zeff record builder for HousePrice records."""
__version__ = "0.0"

import logging
import sqlite3
from zeff.record import *

LOGGER = logging.getLogger("zeffclient.record_builder")


class HousePriceRecordBuilder:
    """Zeff record builder callable object that builds HousePrice records.

    The callable object has a single `config` parameter that the record
    builder understands. This could be a URL, a unique number that is
    a primary key in the database, or a full configuration file.
    """

    def __init__(self, *args, **argv):
        self.conn = sqlite3.connect("db.sqlite3")
        self.conn.row_factory = sqlite3.Row

    def __call__(self, config: str) -> Record:
        LOGGER.info("Begin building ``HousePrice`` record from %s", config)
        record = Record(name=config)
        self.add_structured_items(record, config)
        self.add_unstructured_items(record, config)
        LOGGER.info("End building ``HousePrice`` record from %s", config)
        return record

    def add_structured_items(self, record, id):
        sd = record.structured_data

        # Select all the properties from the database for the record
        sql = f"SELECT * FROM properties WHERE id={id}"
        cursor = self.conn.cursor()
        row = cursor.execute(sql).fetchone()

        # Process each column in the record except for `id` and
        # add it as a structured data item to the structured data
        # object
        for key in row.keys():
            if key == "id":
                continue
            value = row[key]

            # Is the column a continuous or category datatype
            if isinstance(value, (int, float)):
                dtype = StructuredDataItem.DataType.CONTINUOUS
            else:
                dtype = StructuredDataItem.DataType.CATEGORY

            # Create the structured data item and add it to the
            # structured data object
            sdi = StructuredDataItem(name=key, value=value, data_type=dtype)
            sdi.structured_data = sd

        # Clean up then add the structured data object to the record
        cursor.close()

    def add_unstructured_items(self, record, id):
        ud = record.unstructured_data

        # Select all the property imaages for the record
        sql = f"SELECT * FROM property_images WHERE property_id={id}"
        cursor = self.conn.cursor()

        # Process each row returned in the selection, create an
        # unstructured data item, and add that to the unstructured
        # data object. Note that we are assuming that the file-type
        # for all of these images is a JPEG, but that may be different
        # in your system.
        for row in cursor.execute(sql).fetchall():
            url = row["url"]
            file_type = UnstructuredDataItem.FileType.IMAGE
            group_by = row["image_type"]
            udi = UnstructuredDataItem(url, file_type, group_by=group_by)
            udi.unstructured_data = ud

        # Clean up then add the unstructured data object to the record
        cursor.close()


if __name__ == "__main__":
    import sys
    from logging import basicConfig, DEBUG
    import errno
    import argparse
    from zeff.record import format_record_restructuredtext

    if sys.version_info < (3, 7):
        raise Exception("{0} requires Python 3.7.".format(sys.argv[0]))

    basicConfig(level=DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("config", help="URL to information to build HousePrice record")
    options = parser.parse_args()

    try:
        builder = HousePriceRecordBuilder()
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
