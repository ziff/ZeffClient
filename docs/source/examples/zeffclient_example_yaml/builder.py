#!/usr/bin/env python3
"""Zeff record builder for HousePrice records."""
__version__ = "0.0"

import logging
from typing import Optional
import pathlib
import urllib.parse
import yaml
from zeff.record import *

LOGGER = logging.getLogger("zeffclient.record.builder")


class HousePriceRecordBuilder:
    """Record builder for HousePrice records.

    :param arg: A single string argument set in the zeff.conf file. This
        string may be anything the builder understands (e.g. a URL,
        unique number, full configuration file, etc.).
    """

    def __init__(self, arg: str):
        pass

    def __call__(self, model: bool, config: str) -> Optional[Record]:
        """Build and return a record.

        :param model: Flag to indicate if the record builder is building
            records for training or for prediction. If model is true then
            it is for prediction, but if false then it is for training and
            any records not to be used for training should be filtered.

        :param config: A configuration string that was created by the
            record configuration generator.
        """
        urlparts = urllib.parse.urlsplit(config)
        path = pathlib.Path(urlparts[2])
        id = urlparts[3].split("=")[1]
        LOGGER.info("Begin building ``HousePrice`` record from %s", id)
        record = Record(name=id)
        target = self.add_structured_data(record, path, id)
        if not model and not target:
            return None
        self.add_unstructured_data(record, path.parent, id)
        LOGGER.info("End building ``HousePrice`` record from %s", id)
        return record

    def add_structured_data(self, record, path, id):
        target_record = False
        row = None
        with open(path, "r") as ymlstream:
            row = [r for r in yaml.load(ymlstream, Loader=yaml.Loader) if r["id"] == id]
            if len(row) == 0:
                return
            row = row[0]

        # Process each field in the record except for `id` and
        # add it as a structured data to the record object
        for key in row.keys():
            if key == "id":
                continue
            value = row[key]

            # Is the column a continuous or category datatype
            if isinstance(value, (int, float)):
                dtype = DataType.CONTINUOUS
            else:
                dtype = DataType.CATEGORY

            # Is this a target field
            if key in ["estimate_mortgage"] and value is not None:
                target = Target.YES
                target_record = True
            else:
                target = Target.NO

            # Create the structured data item and add it to the record
            sd = StructuredData(name=key, value=value, data_type=dtype, target=target)
            sd.record = record

        return target_record

    def add_unstructured_data(self, record, path, id):

        img_path = path / f"images_{id}"

        # Process each jpeg file in the image path, create an
        # unstructured data, and add that to the record data object.
        for p in img_path.glob("**/*.jpeg"):
            url = f"file://{p}"
            file_type = FileType.IMAGE
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
    parser.add_argument(
        "recordtype",
        choices=["model", "dataset"],
        help="What type of record should be created.",
    )
    parser.add_argument("config", help="Configuration to build HousePrice record")
    options = parser.parse_args()
    config = load_configuration()
    try:
        builderarg = config.records.record_builder_arg
        builder = HousePriceRecordBuilder(builderarg)
        record = builder((options.recordtype == "model"), options.config)
        if options.recordtype == "model" and record == None:
            print("Record is not a training record.")
        else:
            validator = config.records.record_validator((options.recordtype == "model"))
            validator(record)
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
