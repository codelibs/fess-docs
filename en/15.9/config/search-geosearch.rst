==================
Geolocation Search
==================

Overview
========

|Fess| can execute searches with geographical ranges specified for documents containing latitude and longitude location information.
Using this feature, you can search for documents within a certain distance from a specific point,
or build search systems integrated with map services like Google Maps.

Internally, it uses OpenSearch's geo-distance query to filter documents that exist
within a specified distance from a given center point.

Use Cases
=========

Geolocation search can be utilized for purposes such as:

- Store Search: Search for stores near the user's current location
- Real Estate Search: Search for properties within a certain distance from specific stations or facilities
- Event Search: Search for event information around specified locations
- Facility Search: Search for tourist spots or public facilities nearby

Configuration
=============

Index Generation Settings
--------------------------

Location Field Definition
~~~~~~~~~~~~~~~~~~~~~~~~~

In |Fess|, ``location`` is defined as a standard field for storing location information.
This field is configured as OpenSearch's ``geo_point`` type.

Location Registration Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When generating indexes, set latitude and longitude separated by commas in the ``location`` field.

**Format:**

::

    latitude,longitude

**Example:**

::

    45.17614,-93.87341

.. note::
   Specify latitude in the range -90 to 90, and longitude in the range -180 to 180.

Data Store Crawl Configuration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using data store crawl, set latitude and longitude in the ``location`` field from data sources with location information.

**Example: Retrieving from Database**

If latitude and longitude are stored in separate columns, concatenate them into a comma-separated string in SQL.

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

Map the retrieved value to the ``location`` field in the data store configuration script.

::

    location=data.location

Adding Location Information via Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also dynamically add location information to documents using the script feature (Groovy) in crawl configuration.
Assign the value directly to the field name.

::

    // Set latitude and longitude in the location field
    location="35.681236,139.767125"

For details on scripting, refer to :doc:`scripting-groovy`.

Search Settings
---------------

To execute geolocation search, specify the search center point and range in request parameters.

Request Parameters
~~~~~~~~~~~~~~~~~~

The parameter names for geolocation search follow the format ``geo.<field-name>.point`` and ``geo.<field-name>.distance``.
``<field-name>`` is the field name configured in ``query.geo.fields``
(default is ``location``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter Name
     - Description
   * - ``geo.location.point``
     - Latitude and longitude of the search center point (comma-separated. Example: ``35.681236,139.767125``)
   * - ``geo.location.distance``
     - Search radius from center point (with unit. Example: ``10km``)

.. note::
   ``point`` and ``distance`` must be specified together. A ``point`` without ``distance`` is ignored.
   Also, the value of ``point`` must consist of exactly two numeric values (latitude,longitude); an error
   will occur if the format is invalid.

.. note::
   If multiple ``point`` values are specified for the same field, they are treated as OR conditions (within any of the ranges).
   If specified for multiple fields, they are treated as AND conditions (within all of the ranges).

Distance Units
~~~~~~~~~~~~~~

The following units can be used for distance:

- ``km``: kilometers
- ``m``: meters
- ``mi``: miles
- ``yd``: yards

.. note::
   Since the distance value is passed directly to OpenSearch, you can also use other units supported by OpenSearch
   (such as ``cm``, ``mm``, ``ft``, ``in``, ``nmi``).

Sort Order of Search Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Geolocation search operates as a **filter** that narrows results to documents within the specified range.
It does not affect the search score (relevance), and results are not sorted by distance from the center point.
Results are returned in the usual relevance order (or the order specified by the ``sort`` parameter).

.. note::
   |Fess| does not support sorting by distance (nearest-first ordering).
   If you want to display results in distance order, sort them on the client side using the latitude and longitude
   included in the response.

Search Examples
===============

Basic Search
------------

To search for documents within a 10km radius from Tokyo Station (35.681236, 139.767125):

::

    http://localhost:8080/search?q=keyword&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Nearby Search
-------------

To search within 1km from the user's current location:

::

    http://localhost:8080/search?q=ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

API Usage
---------

Geolocation search can also be used with the v2 JSON search API (``/api/v2/search``).
Specify ``geo.location.point`` and ``geo.location.distance`` as request parameters.

::

    curl "http://localhost:8080/api/v2/search?q=hotel&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

Search results are returned in the ``response.data`` array of the common envelope. For details on the API, refer to
:doc:`../api/api-search` and :doc:`../api/api-overview`.

.. note::
   The ``location`` field is not included in the API response by default. To include latitude and longitude in
   the search results, add the following setting to ``fess_config.properties``.

   ::

       query.additional.api.response.fields=location

Field Name Customization
========================

Changing the Default Field Name
--------------------------------

To change the field name used for geolocation search,
change the following setting in ``fess_config.properties``.

::

    query.geo.fields=location

To specify multiple field names, separate them with commas.

::

    query.geo.fields=location,geo_point,coordinates

.. note::
   - Request parameter names correspond to the configured field names. For example,
     if you set ``query.geo.fields=coordinates``, specify ``geo.coordinates.point`` and
     ``geo.coordinates.distance``.
   - Each field specified here must be defined as the ``geo_point`` type in the index mapping.

Implementation Examples
=======================

Web Application Implementation
-------------------------------

Example of retrieving current location and searching using JavaScript:

.. code-block:: javascript

    // Get current location using browser's Geolocation API
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // Build search URL
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // Execute search
        window.location.href = searchUrl;
    });

Google Maps Integration
------------------------

Example of displaying search results as markers on Google Maps:

.. note::
   This example references the ``location`` field from search results. You must configure
   ``query.additional.api.response.fields=location`` in advance so that latitude and longitude
   are included in the response.

.. code-block:: javascript

    // Initialize map
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Execute geolocation search using the Fess v2 search API
    fetch('/api/v2/search?q=store&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // Display search results (response.data array) as markers
            json.response.data.forEach(doc => {
                if (doc.location) {
                    const [lat, lng] = doc.location.split(',').map(Number);
                    new google.maps.Marker({
                        position: {lat: lat, lng: lng},
                        map: map,
                        title: doc.title
                    });
                }
            });
        });

Performance Optimization
========================

Verifying Index Configuration
------------------------------

The location field is defined as the ``geo_point`` type in
``app/WEB-INF/classes/fess_indices/fess/doc.json`` at the installation location.

::

    "location": {
        "type": "geo_point"
    }

Fields of type ``geo_point`` are indexed using a BKD tree, so geo-distance queries
are executed efficiently.

Optimizing Search Range and Response
-------------------------------------

Increasing the search radius increases the number of matching documents within the range,
which may cause longer retrieval and rendering times.

- Set an appropriate search radius according to your use case.
- When handling a large number of results (such as for map display), adjust the page size
  (``num`` parameter) to limit the number of results retrieved.

Troubleshooting
===============

Geolocation Search Not Working
-------------------------------

1. Verify that data is correctly stored in the ``location`` field.
2. Verify that the latitude and longitude format is correct (comma-separated as ``latitude,longitude``; an error will occur if there are not exactly two values).
3. Verify that ``location`` is defined as ``geo_point`` type in OpenSearch index mapping.
4. Verify that both ``point`` and ``distance`` are specified (a ``point`` without ``distance`` is ignored).

No Search Results Returned
---------------------------

1. Verify that documents exist within the specified distance range.
2. Verify that latitude and longitude values are within the correct range (latitude: -90 to 90, longitude: -180 to 180).
3. Verify that distance units are specified correctly.

Location Information Not Included in API Response
--------------------------------------------------

The ``location`` field is not included in the API response by default.
To include latitude and longitude in search results, set
``query.additional.api.response.fields=location`` in ``fess_config.properties``.

Location Information Not Registered Correctly
----------------------------------------------

1. Verify that the ``location`` field is set correctly during crawling.
2. Verify that the latitude and longitude from the data source are being retrieved correctly.
3. When setting location information via script, verify that it is in the string format ``latitude,longitude``.

References
==========

For details on geolocation search, refer to the following resources:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API>`_
