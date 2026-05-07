============
API Overview
============


APIs Provided by |Fess|
========================

This document explains the APIs provided by |Fess|.
By utilizing these APIs, you can use |Fess| as a search server within existing web systems.

Base URL
========

The |Fess| API endpoints are provided at the following base URL:

::

    http://<Server Name>/api/v1/

For example, when running in a local environment, it would be:

::

    http://localhost:8080/api/v1/

Authentication
==============

In the current version, authentication is not required to use the API.
However, you must enable each API through the various settings in the administration screen.

HTTP Methods
============

All API endpoints are accessed using the **GET** method.

Response Format
===============

All API responses are returned in **JSON format** (except for GSA compatible API).
The response ``Content-Type`` is ``application/json``.

Error Handling
==============

When an API request fails, error information is returned along with an appropriate HTTP status code.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: HTTP Status Codes

   * - 200
     - The request was processed successfully.
   * - 400
     - The request parameters are invalid.
   * - 404
     - The requested resource was not found.
   * - 500
     - An internal server error occurred.

Table: HTTP Status Codes

Types of APIs
=============

|Fess| provides the following APIs:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - API for retrieving search results.
   * - popularword
     - API for retrieving popular words.
   * - label
     - API for retrieving a list of created labels.
   * - health
     - API for retrieving server status.
   * - suggest
     - API for retrieving suggested words.

Table: Types of APIs