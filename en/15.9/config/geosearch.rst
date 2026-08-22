===========================
Location Information Search
===========================

Overview
========

You can use location-based search by linking documents with latitude and longitude location information to services like Google Maps.

Configuration
=============

During Indexing
---------------

The `location` field is defined as the field to store location information.
During indexing, set the latitude and longitude in the format such as `45.17614,-93.87341` in the `location` field to register the document.

During Search
-------------

When performing a search using location information, specify values for the request parameters `geo.location.point` and `geo.location.distance`.
Provide latitude and longitude coordinates to `geo.location.point`, and specify the distance from that point to `geo.location.distance`. This allows you to search for data with location information within a certain range from a given point.
The provided values are treated as Double types.

**Example:**

::

    geo.location.point=35.681,139.766&geo.location.distance=10.0km

When specifying this as a request parameter, you can perform a search for documents with location information within a 10km radius from the point (35.681, 139.766).