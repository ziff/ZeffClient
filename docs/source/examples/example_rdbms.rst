========================
ZeffClient RDBMS Example
========================

In this example we will create a record builder that will access an SQL
RDMS database for the information necessary to create the record.


Record Config Generator
=======================

A record config generator will generate a string that will be passed
to the record builder. This string may be a URL, a unique id, or a full
configuration file.

For this example we will use the id that is the primary key of the
properties table in the SQLite database:

   ``1395678``



Record Builder
==============

1. Download an decompress :download:`example_rdbms.tar.bz2 <example_rdbms.tar.bz2>`
   into a location of your choice.

2. Change to the directory that was created. This will be the ``<root>``
   used in the URL.

3. Setup virtual environment:

   A. ``python -m venv .venv``

   B. ``pip install --upgrade pip``

   C. ``pip install git+ssh://git@github.com/ziff/ZeffClient.git``

      .. note::

         This step will change when the repository becomes public
         and ZeffClient is available in PyPi.

4. ``zeff template --help``
   This will show the various options availalble when working with
   templates.

5. ``zeff template HousePrice > house_price_record_builder.py``
   Create a new house price record builder python file from a template.

   A. This file may be executed from the command line directly and has a
      basic command line interface using ``argparse``. This will aid you
      in writing and debugging your record building, because you may
      work with a single record without needing the entire ZeffClient
      system.

   B. This file will have a new class `HousePriceRecordBuilder` where you
      will write all the code to build a new record for house prices. This
      class will create a callable object that takes a single URL parameter
      that you will define in the URL Generator.

   C. The class uses the `zeffclient.record_builder` logger (`LOGGER`) to
      indicate various stages of the record building process. You should
      also use this logger while building records for error reporting,
      warnings, information, and debugging.

6. ``python house_price_record_builder.py 1395678`` should show the following
   output:

   ::

      INFO:zeffclient.record_builder:Begin building ``HousePrice`` record from 1395678
      INFO:zeffclient.record_builder:End building ``HousePrice`` record from 1395678
      ======================
      Record(name='Example')
      ======================

7. Build an empty record:

   A. In ``def __call__(...)`` change ``Record(name="example")`` to:

      ::

         record = Record(name=config)

   B. When you execute this it should print the same as in step 6, but with
      "Example" changed to the record number.

8. Setup database access:

   A. In the ``import`` section add ``import sqlite3``.

   B. In ``def __init__(...)`` replace ``pass`` with:

      ::

         self.conn = sqlite3.connect("db.sqlite3")
         self.conn.row_factory = sqlite3.Row

   C. When you execute this it should print out the same as in step 7
      with no errors.

9. Add structured items to the record:

   A. In ``def __call__(...)`` replace ``# Your record build code goes here``
      with:

      ::

         self.add_structured_items(record, config)

   B. Then add the following method:

      ::

         def add_structured_items(self, record, id):

             # Create a new structured data element
             sd = StructuredData()

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
             sd.record = record

   C. When you execute this you should see everything from step 8 with
      additional structured data table that will look similar to, but
      with more table entries:

      ::

          Structured Data
          ===============
          +-----------------+------------+--------+-------+
          | name            | data_type  | target | value |
          +=================+============+========+=======+
          | garage_capacity | CONTINUOUS | NO     | 6     |
          +-----------------+------------+--------+-------+

10. Add unstructured items to the record:

    A. In ``def __call__(...)`` add the following after the line you
       added in step 8.

       ::

          self.add_unstructured_items(record, config)

    B. Then add the following method:

       ::

          def add_unstructured_items(self, record, id):

              # Create an unstructured data object
              ud = UnstructuredData()

              # Select all the property imaages for the record
              sql = f"SELECT * FROM property_images WHERE property_id={id}"
              cursor = self.conn.cursor()

              # Process each row returned in the selection, create an
              # unstructured data item, and add that to the unstructured
              # data object. Note that we are assuming that the media-type
              # for all of these images is a JPEG, but that may be different
              # in your system.
              for row in cursor.execute(sql).fetchall():
                  url = row["url"]
                  media_type = "image/jpg"
                  group_by = row["image_type"]
                  udi = UnstructuredDataItem(url, media_type, group_by=group_by)
                  udi.unstructured_data = ud

              # Clean up then add the unstructured data object to the record
              cursor.close()
              ud.record = record

    C. When you execute this you should see everything from step 8 with
       additional structured data table that will look similar to, but
       with more table entries:

       ::

           Unstructured Data
           =================
           +------------+------------+----------------------------------+
           | media_type | group_by   | data                             |
           +============+============+==================================+
           | image/jpg  | home_photo | https://example.com/photo_38.jpg |
           +------------+------------+----------------------------------+

