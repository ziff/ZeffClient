Project Directory
-----------------

The project directory has a virtual environment setup in ``.venv`` by
the ``quickstart.sh`` script. This environment has had ZeffClient
installed. This may be activated at any time by
``source .venv/bin/activate``.

The steps taken to setup the directory are:

   1. ``python -m venv .venv``

   2. ``source .venv/bin/activate``

   3. ``pip install --upgrade pip``

   4. ``pip install git+ssh://git@github.com/ziff/ZeffClient.git``

      .. note::

         This step will change when the repository becomes public
         and ZeffClient is available in PyPi.

The main command to work with ZeffClient is ``zeff``. To quickly see
what options and subcommands are available use ``zeff --help``.
