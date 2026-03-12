=========================
Geolocation-Based Search
=========================

By adding latitude and longitude geolocation information to each document during index generation, you can perform searches using geolocation information.

Usage
-----

By default, the following parameters are available:

.. list-table::

   * - geo.<fieldname>.point
     - Specify latitude and longitude in degrees as Double type.
   * - geo.<fieldname>.distance
     - Specify distance from document in kilometers. Example: 10km

Table: Request Parameters
