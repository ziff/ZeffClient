========================
ZeffClient RDBMS Example
========================

In this example we will create a record builder that will access an SQL
RDMS database for the information necessary to create the record.


QuickStart
==========

This quickstart will download the example archive, unarchive it, change
into the new directory, and then run a script in that directory that
will do the rest of the example. At this point you will be asked some
questions by the ``zeff init`` command — you will need to enter your
``org_id`` and ``user_id`` that your received from Zeff, but all
other questions you may accept the defaults by hitting enter.

Steps
-----

   1. Download: :download:`zeffclient_example_rdbms.tar.bz2 <zeffclient_example_rdbms.tar.bz2>`

   2. Decompress: ``tar -xjf zeffclient_example.rdbms.tar.bz2``

   3. Change directory: ``cd zeffclient_example_rdbms``

   4. Run quickstart script: ``./quickstart.sh``


How it Works
============

.. include:: project_directory.rst


Record Config Generator
-----------------------

The ``generator.HousePriceRecordGenerator`` in ``generator.py`` will
yield each ``id`` that is selected from the ``properties`` table.
For this example it only returns the string that is the ``id``, but
it is not limited to strings and could be a URL, file, etc.

For this particular example there is only one row in the ``properties``
table and the ``id`` for that row is ``1395678``.

To test the generator by itself use the command ``./generator.py`` or
``python generator.py``.


Record Builder
--------------

The ``builder.HousePriceRecordBuilder`` in ``builder.py`` will take
the configuration string given by the record config generator and
will yield a record.

The file ``builder.py`` may be executed from the command line directly,
and has a basic command line interface using ``argparse``. This will
aid you in writing and debugging your record builder, because you
may work with a single record without needing to run the entire
ZeffClient system.

The module uses the `zeffclient.record.builder` logger to indicate
various stages of the record building process. You should also use
this logger while building records for error reporting, warnings,
information, and debugging.

The file ``builder.py`` has a class `HousePriceRecordBuilder` where
all the code to build a new record for house prices is contained. This
class will create a callable object that takes a single argument that
has been yielded by the record generator. It has three steps: create
a new record, add structured data to the record, and add unstructured
data to the record.

.. include:: zeffclient_example_rdbms/builder.py
   :code: python
   :number-lines: 24
   :start-line: 23
   :end-line: 31

Adding structured data is done through a select on the `properties`
table in the database and then converting each returned column
(except `id`) into a structured data item.

.. include:: zeffclient_example_rdbms/builder.py
   :code: python
   :number-lines: 32
   :start-line: 31
   :end-line: 59

Adding unstructured data is done through a select on the
`property_images` table in the databse and then creating an
unstructured data item.

.. include:: zeffclient_example_rdbms/builder.py
   :code: python
   :number-lines: 60
   :start-line: 59
   :end-line: 79
