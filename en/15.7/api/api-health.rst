==========
Health API
==========

This document describes the v2 Health API of |Fess|.
For the common response envelope and error model, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

Fetching Status
===============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/health``
==================  ====================================================

Returns a snapshot of the search engine cluster status (``monitor`` tag).
The HTTP status is 200 when the cluster status is ``green`` or ``yellow``, and 503 when it is ``red``.

This endpoint respects the envelope invariant "``status >= 1`` ⇔ HTTP status ``>= 400``".

- When ``green`` or ``yellow``: returns a success envelope (``status: 0``) with ``engine``.
- When ``red``: returns an error envelope (``status: 9``, ``error.code: service_unavailable``) with the engine snapshot embedded under ``error.details.engine`` (to allow monitoring tools to parse cluster metadata).

The fields of ``engine`` are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine Fields

   * - ``cluster_name``
     - Cluster name (str).
   * - ``status``
     - Cluster status. One of ``green``, ``yellow``, or ``red``.
   * - ``ping_status``
     - Ping status (int).

Table: engine Fields

Request Parameters
------------------

There are no available request parameters.

Response
--------

When the cluster is ``green`` or ``yellow`` (200), a success envelope with ``engine`` is returned.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

When the cluster is ``red`` (503), an error envelope is returned with the engine snapshot embedded under ``error.details.engine``.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "Cluster is unavailable.",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
              "ping_status": 2
            }
          }
        }
      }
    }

Usage Examples
==============

Request example using curl:

::

    curl "http://localhost:8080/api/v2/health"

Response and Error Response
============================

For details on the error model, see :doc:`api-overview`. The HTTP statuses returned by this endpoint are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response List

   * - Status Code
     - Description
   * - 200 OK
     - Cluster is ``green`` or ``yellow`` and reachable. The success envelope contains ``engine``.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 503 Service Unavailable
     - Cluster is ``red``. An error envelope (``error.code: service_unavailable``) with the engine snapshot under ``error.details.engine``.

Table: Response List
