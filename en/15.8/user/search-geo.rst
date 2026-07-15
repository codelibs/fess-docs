==========================
Geolocation-Based Search
==========================

By attaching latitude and longitude geolocation information to each document during index generation, you can filter search results based on the distance from a specified point at search time.

Overview
--------

Geolocation-based search includes in the search results only those documents that fall within a radius centered on a specified point (latitude and longitude). This filtering is applied as a filter using OpenSearch's geo_distance query, so it does not affect the score (relevance). Also, sorting by distance is not supported.

The field that stores geolocation information must be defined as the ``geo_point`` type in the OpenSearch mapping. By default, the ``location`` field is provided as the ``geo_point`` type. However, since no built-in process is provided to populate the ``location`` field with a value, you must populate the geolocation information yourself, using data store crawling field mappings or scripts, the API for registering documents with the search engine, or similar means.

Usage
-----

Geolocation-based search is specified by adding the following parameters to the search request. By default, it can be used with the ``location`` field.

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - ``geo.<fieldname>.point``
     - Specify the latitude and longitude of the center point in the format ``latitude,longitude``. The value consists of two comma-separated numbers in decimal degrees (Double type). Example: ``35.681236,139.767125``
   * - ``geo.<fieldname>.distance``
     - Specify the distance (radius) from the center point. Example: ``10km``

Table: Request Parameters

For ``<fieldname>``, specify the name of the field that stores geolocation information. Only fields registered in ``query.geo.fields`` can be specified, and by default this is ``location``. To use a different field, map it as the ``geo_point`` type, and add it to ``query.geo.fields`` in ``fess_config.properties``, separated by commas.

For example, to search for documents within a 10km radius from latitude 35.681236 and longitude 139.767125 (near Tokyo Station), add the following parameters to the search request.

::

    geo.location.point=35.681236,139.767125&geo.location.distance=10km

Distance Units
--------------

The value of ``geo.<fieldname>.distance`` is interpreted as an OpenSearch distance unit. In addition to ``km`` (kilometers), you can use ``mm``, ``cm``, ``m``, ``in``, ``ft``, ``yd``, ``mi`` (miles), ``nmi`` (nautical miles), and others. If you omit the unit and specify only a number, it is treated as meters (for example, ``500`` means 500 meters).

Specifying Multiple Conditions
-------------------------------

* If you specify ``geo.<fieldname>.point`` multiple times for the same field, documents that fall within the radius of any of the points are searched (OR condition).
* If you specify geolocation information for different fields, documents that satisfy all of the conditions are searched (AND condition).

.. note::

   Both ``geo.<fieldname>.point`` and ``geo.<fieldname>.distance`` must be specified. If ``distance`` is not specified, the corresponding ``point`` condition is ignored. In addition, an error occurs if the value of ``point`` is not in the ``latitude,longitude`` format (two comma-separated numbers) or cannot be interpreted as numbers.
