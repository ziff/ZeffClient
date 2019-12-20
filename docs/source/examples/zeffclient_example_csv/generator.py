#!/usr/bin/env python3
"""Zeff record config generator for HousePrice records."""
import logging
import urllib.parse
import csv

LOGGER = logging.getLogger("zeffclient.record.generator")


def HousePriceRecordGenerator(arg: str):
    """Return house primary key value."""
    with open(arg, "r") as csvfile:
        for row in csv.DictReader(csvfile):
            url = f"file://{arg}/?id={row['id']}"
            yield url


if __name__ == "__main__":
    from logging import basicConfig, DEBUG
    from zeff.cli import load_configuration

    basicConfig(level=DEBUG)

    config = load_configuration()
    generatorarg = config.records.records_config_arg
    for config in HousePriceRecordGenerator(generatorarg):
        print(config)
