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
The HTTP status is 200 when the cluster status is ``GREEN`` or ``YELLOW``, and 503 when it is ``RED`` or when the search engine cannot be reached.

This endpoint respects the envelope invariant "``status >= 1`` ⇔ HTTP status ``>= 400``".

- When ``GREEN`` or ``YELLOW``: returns a success envelope (``status: 0``) with ``engine``.
- When ``RED``: returns an error envelope (``status: 9``, ``error.code: service_unavailable``) with the engine snapshot embedded under ``error.details.engine`` (to allow monitoring tools to parse cluster metadata).
- When the search engine cannot be reached: returns an error envelope in the same way as ``RED`` (``error.code: service_unavailable``, ``error.message: search engine is not reachable``), with ``status: UNAVAILABLE`` and ``ping_status: 1`` in ``error.details.engine``.

The fields of ``engine`` are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine Fields

   * - ``status``
     - Cluster status. One of ``GREEN``, ``YELLOW``, or ``RED`` (upper case). ``UNAVAILABLE`` when the search engine cannot be reached.
   * - ``ping_status``
     - Ping status (int). It is ``1`` when the cluster status is ``RED`` or the search engine cannot be reached, and ``0`` otherwise (``GREEN`` or ``YELLOW``).

Table: engine Fields

The cluster name (``cluster_name``) is not returned, because this endpoint can be called without authentication.

Request Parameters
------------------

There are no available request parameters.

Response
--------

When the cluster is ``GREEN`` or ``YELLOW`` (200), a success envelope with ``engine`` is returned.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

When the cluster is ``RED`` (503), an error envelope is returned with the engine snapshot embedded under ``error.details.engine``.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
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
     - Cluster is ``GREEN`` or ``YELLOW`` and reachable. The success envelope contains ``engine``.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 503 Service Unavailable
     - Cluster is ``RED`` or the search engine cannot be reached. An error envelope (``error.code: service_unavailable``) with the engine snapshot under ``error.details.engine``.

Table: Response List
