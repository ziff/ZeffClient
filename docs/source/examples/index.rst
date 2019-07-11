Examples
========

.. toctree::
   :maxdepth: 2

   Record RDBMS <example_rdbms>
   Record YAML <example_yaml>
   Record CSV <example_csv>

The examples contained in this directory are designed to show you how
to build a record for training and inference in Zeff Cloud API.

The sub-directories will have details on how to build a record from a
relational database (`rdbms`), a CSV file (`csv`), or a YAML file
(`yaml`).

This readme applies to all examples and will explain the overall
process for buildling a record and how a record relates to other
objects.


Process
=======

.. uml::
   :scale: 50 %
   :align: center

   @startuml
   ZeffClient -> RecordConfigGenerator: next()
   RecordConfigGenerator --> ZeffClient: config_string
   ZeffClient -> RecordBuilder: config_string
   RecordBuilder -> RecordBuilder: create record with name
   RecordBuilder -> RecordBuilder: create and add structured data items
   RecordBuilder -> RecordBuilder: create and add unstructured data items
   RecordBuilder --> ZeffClient: record
   @enduml


ZeffClient
==========

This is the application that will coordinate building, validation, and
uploading of records to the Zeff Cloud API. This is meant to reduce the
amount of infrastructure you need to build in order to use Zeff Cloud.


Record Config Generator
=======================

This is a generator object you will build that will generate
configuration strings. These strings will be used by ZeffClient
as a parameter to a record builder in order to create a single
record. This is not necessary when running a record builder directly,
but is needed by ZeffClient.

Having this separate from the record builder allows ZeffClient to
control record building so multiple records may be built in parallel
to allow improved throughput to Zeff Cloud.

The configuration strings may contain anything you choose, but must
be acceptable to the assocaited record builder when it is called.

There are generators in :doc:`../zeff.recordgenerator` that may be
used for common types of configuration strings such as URLs.


Record Builder
==============

This is a class that you will create that ZeffClient will create a
record builder object. These objects must be callable with a single
configuration string parameter that has been generated from a record
config generator, and will return a single record object.

The use of a template (e.g. ``zeff template My``) will provide Python
source that will allow the file to be executed to create a single
record, and to be used by ZeffClient. The file execution will allow
you to make work on a single record at a time without the necessity
of running the entire ZeffClient system.


Record
======

A record object is built from classes in :doc:`../zeff.record`. An
object of this type is required to be returned from your record
builder.

A record object is a composition of structured and unstructured
data.

.. uml:: ../uml/recordClassDiagram.uml
   :scale: 50 %
   :align: center

