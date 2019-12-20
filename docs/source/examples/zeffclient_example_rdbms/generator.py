#!/usr/bin/env python3
"""Zeff record config generator for HousePrice records."""
import logging
import sqlite3

LOGGER = logging.getLogger("zeffclient.record.generator")


def HousePriceRecordGenerator(arg: str):
    """Return house primary key value."""
    LOGGER.debug("Open database connection to %s", arg)
    conn = sqlite3.connect(arg)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM properties")
    rows = cursor.fetchmany()
    while rows:
        for row in rows:
            id = row["id"]
            LOGGER.debug("House property id %s", id)
            yield id
        rows = cursor.fetchmany()


if __name__ == "__main__":
    from logging import basicConfig, DEBUG
    from zeff.cli import load_configuration

    basicConfig(level=DEBUG)

    config = load_configuration()
    generatorarg = config.records.records_config_arg
    for config in HousePriceRecordGenerator(generatorarg):
        print(config)
