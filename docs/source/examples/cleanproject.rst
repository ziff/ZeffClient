Project Setup
=============

1. Install or update Python to a minimum of version 3.7.

2. Create project directory and change to directory.

3. Python virtual environment.

   A. Create environment: ``python3 -m venv .venv``.

   B. Activate environment: ``source .venv/bin/activate``

   C. Update pip: ``pip install --upgrade pip``

4. Install ZeffClient: ``pip install git+ssh://git@github.com/ziff/ZeffClient.git``.

      .. note::

         This step will change when the repository becomes public
         and ZeffClient is available in PyPi. The command will change
         to ``pip install ZeffClient``.

5. Initialize the ZeffClient project: ``zeff init``.

   A.
