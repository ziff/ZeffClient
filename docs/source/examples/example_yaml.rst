=======================
ZeffClient YAML Example
=======================

In this example we will create a record builder that will access a
CSV file for information necessary to create the record.


Record Config Generator
=======================

A record config generator will generate a string that will be passed
to the record builder. This string may be a URL, a unique id, or a full
configuration file.

For this example we will use a URL that identifies the CSV file to
access with a query section that gives the id of the row that we will
use:

   ``file:///<root>/properties.yml?id=1395678``

The ``<root>`` must be replaced with the path to the directory that
contains your ``properties.yml`` file. In this example that will be
the directory you create in step 1 of `Record Builder`_.


Record Builder
==============

1. Download an decompress :download:`example_yaml.tar.bz2 <example_yaml.tar.bz2>`
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

6. Directory structure:

   A. The YAML information is contained in ``./properties.yml``.

   B. Images that will be added to the record are in ``./images_1395678``.

7. ``python house_price_record_builder.py "file:///<root>/properties.yml?id=1395678`` should show the following
   output:

   ::

      INFO:zeffclient.record_builder:Begin building ``HousePrice`` record from file:///<root>/properties.yml?id=1395678
      INFO:zeffclient.record_builder:End building ``HousePrice`` record from file:///<root>/properties.yml?id=1395678
      ======================
      Record(name='Example')
      ======================

8. Build an empty record:

   A. In the ``import`` section add

      ::

         import pathlib
         import urllib.parse

   B. Change ``def __call__(...)`` to be:

      ::

        urlparts = urllib.parse.urlsplit(config)
        path = pathlib.Path(urlparts[2])
        id = urlparts[3].split('=')[1]
        LOGGER.info("Begin building ``HousePrice`` record from %s", id)
        record = Record(name=id)
        # Your record build code goes here
        LOGGER.info("End building ``HousePrice`` record from %s", id)
        return record

   C. When you execute this it should print the same as in step 6, but with
      "Example" changed to the record number and the log entries using the
      record number.

9. Add structured items to the record:

   A. In the ``import`` section add ``import yaml``.

   B. In ``def __call__(...)`` replace ``# Your record build code goes here``
      with:

      ::

         self.add_structured_items(record, path, id)

   C. Then add the following method:

      ::

         def add_structured_items(self, record, path, id):
             row = None
             with open(path, 'r') as ymlstream:
                 row = [r for r in yaml.load(ymlstream) if r['id'] == id]
                 if len(row) == 0:
                     return
                 row = row[0]

             # Create a new structured data element
             sd = record.structured_data

             # Process each field in the record except for `id` and
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

   D. When you execute this you should see everything from step 8 with
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

    A. In ``def __call__(...)`` add the following after the line created
       in step 8:

       ::

          self.add_unstructured_items(record, path.parent, id)

    B. Then add the following method:

       ::

          def add_unstructured_items(self, record, path, id):

              img_path = path / f"images_{id}"

              # Create an unstructured data object
              ud = record.unstructured_data

              # Process each jpeg file in the image path, create an
              # unstructured data item, and add that to the unstructured
              # data object. Note that we are assuming that the media-type
              # for all of these images is a JPEG, but that may be different
              # in your system.
              for p in img_path.glob('**/*.jpeg'):
                  url = f"file://{p}"
                  media_type = "image/jpg"
                  group_by = "home_photo"
                  udi = UnstructuredDataItem(url, media_type, group_by=group_by)
                  udi.unstructured_data = ud

    C. When you execute this you should see everything from step 8 with
       additional structured data table that will look similar to, but
       with more table entries:

       ::

           Unstructured Data
           =================
           +------------+----------+----------------------------------------+
           | media_type | group_by | data                                   |
           +============+==========+========================================+
           | image/jpg  | None     | file://images_1395678/property003.jpeg |
           +------------+----------+----------------------------------------+


