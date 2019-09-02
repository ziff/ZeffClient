############
Installation
############

.. toctree::
   :hidden:


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


Documentation
-------------

Building documentation requires installation of some tools. This installation
must be done through your system's package manager (e.g. MacPorts, Brew,
apt-get, etc).

   - plantuml
   - graphviz
