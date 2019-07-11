Glossary
========

.. toctree::
   :hidden:

.. glossary::

   Record
      An object that holds structured and unstructured data for use in
      training the model and for making inferences.

   Record Builder
      An callable object that takes a string parameter that will create
      a single record and return it. One or more record builders may be
      executing at the same time in multiple processes.

   Record Config Generator
      A generator object that will return configuration strings which
      will be used as a parameter when calling a record builder. The
      purpose for this separation is to allow record building to be
      run in parallel.

   Structured Data
      A key-value mapping object that adds data typing to the value, adn
      marks the data as being used in training, in inference, or should be
      ignored.

   Unstructured Data
      An object that has a URL reference to data with a specified media-type
      and may be grouped with other unstructured data.
