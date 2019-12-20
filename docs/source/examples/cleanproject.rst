Project Setup
=============

1. Install or update Python to a minimum of version 3.7.

2. Create project directory and change to directory.

3. Python virtual environment.

   A. Create environment:
          ``python3 -m venv .venv``

   B. Activate environment:
          ``source .venv/bin/activate``

   C. Update pip:
          ``pip install --upgrade pip``

4. Install ZeffClient:
       ``pip install git+ssh://git@github.com/ziff/ZeffClient.git``

      .. note::

         This step will change when the repository becomes public
         and ZeffClient is available in PyPi. The command will change
         to ``pip install ZeffClient``.

5. Initialize the ZeffClient project based on the type of project:
   generic, geospatial, or temporal. To see all options for init
   use ``zeff init --help``.

   A. Project type examples:

      a. For a generic project use ``zeff init generic``.

      b. For a geospatial project use ``zeff init geospatial``.

      c. For a temporal project use ``zeff init temporal``.

   B. Answer the configuration questions (defaults or current
      current configuration values will be shown in ``[]`` and
      may be accepted by hitting enter):

      a. ``Server URL []?``: This is the server URL where records,
         datasets, models, etc will be located. The default shown
         is usually sufficient for all projects.

      b. ``Organization ID []?``: use the org id that you were given.

      c. ``User ID []?``: use your user id.

      d. ``Dataset Title []?``: unique name for your new project.

      e. ``Dataset Description []?``: description of your new project.

      f. ``Configuration generator python name []?``: the configuration
         generator python name. For example ``generator.Spam`` will
         create a file ``generator.py`` in the current directory that
         will have a generator function named ``Spam``.

      g. ``Configuration generator init argument []?``: an argument to
         give to your generator when it is created. This may be left
         empty.

      h. ``Record builder python name []?``: the record builder python
         name. For example ``builder.Parrot`` will create a file
         ``builder.py`` in the current directory that will contain a
         class named ``Parrot``.

      i. ``Record builder init argument []?``: an argument to give to
         your builder when it is created. This may be left empty.

      j. ``Record validator python name []?``: the validator python
         name. The default that will be shown in the ``[]`` will
         usually be sufficient for most projects.

6. Edit and test the configuration generator file (e.g. ``generator.py``):

   A. To test the generator by executing the file: ``python generator.py``.
      This will output each generated string on a single line. Before any
      changes are made this will output a single line that will show the
      generator configuration argument in the ``zeff.conf`` file.

   B. Edit the generator function (e.g. ``def Spam(arg: str):``) to read
      from your data source to create a unique string that your builder
      will be able to use to create records. See the RDBMS, YMAL, or
      CSV example projects to see how this would be done.

7. Edit and test the builder file (e.g. ``builder.py``):

   A. To test the builder by executing the file: ``python builder.py``.
      The required argument is a string that would be created by the
      generator you edited in the previous step. Before any changes
      are made this will print out a record with a name of "example".

   B. The builder may have an optional version associated with it by
      changing the ``__version__`` field at the top of the file. This
      is only for your use and is not used by ZeffClient.

   C. The builder class (e.g. ``class Parrot:``) is where you will do
      all the work necessary to create records. This class will be
      given the record builder argument in the ``zeff.conf`` file and
      it must create a callable object that when called will accept
      a flag that indicates a record should be for a dataset or a model,
      a configuration string that was created by the configuration
      generator, and will return a ``zeff.record.Record`` object.

   D. The code after the ``if __name__ == "__main__":`` script protection
      block exists to help you test building records, or in debugging
      records that have failed to build during a run of ZeffClient.
      Feel free to make any changes in this code to make things easier
      for you.
