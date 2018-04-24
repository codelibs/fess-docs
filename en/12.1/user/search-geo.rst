==========
Geo Search
==========

Geo Search
==========

|Fess| supports Geo Search to search documents with location information.
To perform Geo search, indexed document needs to contains values of latitude and longitude in location field.

Usage
----

Geo information is passed as request parameters.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - geo.<fieldname>.point
     - Comma-separated value that is latitude,longitude.
   * - geo.<fieldname>.distance
     - Distance from the above point.

Table: Request parameters


