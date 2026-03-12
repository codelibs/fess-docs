==================
Geolocation Search
==================

Overview
========

|Fess| can execute searches with geographical ranges specified for documents containing latitude and longitude location information.
Using this feature, you can search for documents within a certain distance from a specific point,
or build search systems integrated with map services like Google Maps.

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

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

Adding Location Information via Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also dynamically add location information to documents using the script feature in crawl configuration.

::

    // Set latitude and longitude in location field
    doc.location = "35.681236,139.767125";

Search Settings
---------------

To execute geolocation search, specify the search center point and range in request parameters.

Request Parameters
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter Name
     - Description
   * - ``geo.location.point``
     - Latitude and longitude of the search center point (comma-separated)
   * - ``geo.location.distance``
     - Search radius from center point (with unit)

Distance Units
~~~~~~~~~~~~~~

The following units can be used for distance:

- ``km``: kilometers
- ``m``: meters
- ``mi``: miles
- ``yd``: yards

Search Examples
===============

Basic Search
------------

To search for documents within a 10km radius from Tokyo Station (35.681236, 139.767125):

::

    http://localhost:8080/search?q=search keyword&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Nearby Search
-------------

To search within 1km from the user's current location:

::

    http://localhost:8080/search?q=ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Sorting by Distance
-------------------

To sort search results by distance, use the ``sort`` parameter.

::

    http://localhost:8080/search?q=convenience store&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

API Usage
---------

Geolocation search can also be used with the JSON API.

::

    curl -X POST "http://localhost:8080/json/?q=hotel" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

Field Name Customization
========================

Changing Default Field Name
----------------------------

To change the field name used for geolocation search,
change the following setting in ``fess_config.properties``.

::

    query.geo.fields=location

To specify multiple field names, separate them with commas.

::

    query.geo.fields=location,geo_point,coordinates

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

.. code-block:: javascript

    // Initialize map
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Execute geolocation search with Fess API
    fetch('/json/?q=store&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // Display search results as markers
            data.response.result.forEach(doc => {
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

Index Configuration Optimization
---------------------------------

When handling large amounts of location data, optimize index configuration.

Check location field settings in ``app/WEB-INF/classes/fess_indices/fess.json``.

::

    "location": {
        "type": "geo_point"
    }

Limiting Search Range
---------------------

Considering performance, it is recommended to set the search range to the minimum necessary.

- Wide-range searches (50km or more) may take time to process
- Set appropriate ranges according to use case

Troubleshooting
===============

Geolocation Search Not Working
-------------------------------

1. Verify that data is correctly stored in the ``location`` field.
2. Verify that the latitude and longitude format is correct (comma-separated).
3. Verify that ``location`` is defined as ``geo_point`` type in OpenSearch index mapping.

No Search Results Returned
---------------------------

1. Verify that documents exist within the specified distance range.
2. Verify that latitude and longitude values are within the correct range (latitude: -90 to 90, longitude: -180 to 180).
3. Verify that distance units are specified correctly.

Location Information Not Displayed Correctly
---------------------------------------------

1. Verify that the ``location`` field is set correctly during crawling.
2. Verify that the data type for latitude and longitude in the data source is numeric.
3. When setting location information via script, verify that the string concatenation format is correct.

References
==========

For details on geolocation search, refer to the following resources:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
