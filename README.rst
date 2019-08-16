**********
ZeffClient
**********

.. image:: https://img.shields.io/pypi/v/ZeffClient
   :alt: PyPI Version
   :target: https://pypi.org/project/ZeffClient

.. image:: https://img.shields.io/pypi/pyversions/ZeffClient
   :alt: Python Versions
   :target: https://pypi.org/project/ZeffClient

.. image:: https://g.codefresh.io/api/badges/pipeline/dgonzo/ZeffClient%2Fci_zeffclient?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWNlNDNhMDQ2MGNmOGMxZTZmY2NhNGVm.Hg2iF4tMbJKQVS6C019WtitMwcJckIdD1bK8NlYaM_c&type=cf-1
   :alt: codefresh Status
   :target: https://g.codefresh.io/pipelines/ci_zeffclient/builds?repoOwner=ziff&repoName=ZeffClient&serviceName=ziff%2FZeffClient&filter=trigger:build~Build;branch:master;pipeline:5d0bdd0db5092ffa8c954a30~ci_zeffclient

.. Badge Coverage

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Black Code Style
   :target: https://github.com/python/black

.. image:: https://img.shields.io/github/commits-since/ziff/ZeffClient/latest.svg
   :alt: Commits Since
   :target: https://github.com/ziff/ZeffClient/commits/

.. image:: http://pepy.tech/badge/ZeffClient
   :alt: PyPi Downloads
   :target: https://pepy.tech/project/ZeffClient


Announcements
=============



Overview
========

ZeffClient is a collection of libraries and tools to make working with
Zeff Cloud API online systems easier.

   - ``zeff`` is a Python package that simplifies the creation,
     modification, and uploading of records to Zeff Cloud API.

   - ``zeff/record`` is a package for building records that may
     be validated or uploaded to Zeff Cloud API.

   - ``zeff/cli`` is a CLI tool that simplifies experimentation
     with Zeff Cloud API.


Requirements
------------

- Python 3.7


Installing
----------

TBW

Library
-------

TBW

Commandline
-----------

TBW


Build
=====

Common build steps are defined in ``Makefile`` and may be listed by
executing ``make help`` on the command line.

Most tools necessary for make commands will be installed via ``pip`` into
the active python environment.


virtualenv
----------

It is recommended that a virtualenv be created and activated before
executing any make commands.

   1. ``python3 -m venv .venv``
   2. ``source .venv/bin/activate``


make docs
---------

Building documentation requires installation of some tools. This installation
must be done through your system's package manager (e.g. MacPorts, Brew,
apt-get, etc).

   - plantuml
   2. graphviz


Change Log
==========


Contributing
============

Before creating your first commit:

   1. Install `pre-commit <https://pre-commit.com>`_.
   2. Execute ``pre-commit install``

Before creating any commit:

   1. ``make validate``



:copyright: |copy| 2019 Ziff, Inc.


.. |copy| unicode:: 0xA9 .. copyright sign

