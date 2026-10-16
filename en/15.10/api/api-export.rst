========================
Search Result Export API
========================

This document describes the v2 Export API of |Fess|, which downloads search results as a CSV or
JSON file. For the common response envelope and error model, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   Export is disabled by default. To use it, set ``api.search.export=true`` in
   ``fess_config.properties``. When it is enabled, the bundled ``bootstrap`` theme shows an export
   menu (CSV / JSON) beside the result count. ``features.search_export`` of ``/api/v2/ui/config``
   reports the state.

Downloading Search Results
==========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/export``
==================  ====================================================

Returns the documents matching the search as a file download (``Content-Disposition: attachment``,
file name ``search_results.csv`` or ``search_results.json``).

- The same role filter as ``/api/v2/search`` applies. With ``login.required=true``, an access token
  can be used the same way as with ``/api/v2/search``.
- At most ``api.search.export.max.size`` (default: ``1000``) documents are exported. The paging
  parameters (``start``, ``num``) are not used.
- The exported fields are those in ``api.search.export.fields`` (default:
  ``title,url_link,last_modified,content_length,filetype``) that may also appear in API responses.
- Requests are limited to ``api.search.export.rate.limit.per.minute`` (default: ``10``; ``0`` means
  unlimited) per minute, counted per logged-in user, or per client IP for a guest. Over the limit the
  endpoint answers ``429`` with a ``Retry-After`` header.
- An export is not recorded in the search log.

Request Parameters
------------------

The same search condition parameters as ``/api/v2/documents/all`` can be given, such as ``q``,
``ex_q``, ``fields.*``, ``sort`` and ``lang`` (see :doc:`api-search`). In addition:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``format``
     - File format: ``csv`` (default) or ``json``. Any other value produces ``invalid_request`` (400).

Table: Request Parameters

Response
--------

The CSV file has a header row of field names and is written in the encoding of
``csv.file.encoding`` (a UTF-8 file starts with a byte order mark). A value that starts with ``=``,
``+``, ``-``, ``@``, a tab or a carriage return gets a leading ``'`` so that a spreadsheet does not
run it as a formula. A multi-valued field is joined with a space.

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

The JSON file is ``{"data":[{...},...]}``, and multi-valued fields stay arrays.

A failure before the file starts returns the usual error envelope. A failure after that cannot be
reported in the file, so the download ends early: a truncated CSV, or JSON that does not parse.

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - A malformed query, a ``format`` other than ``csv`` / ``json``, or export disabled with
       ``api.search.export=false``.
   * - 401 Unauthorized
     - When authentication is required (for example, an anonymous caller with ``login.required=true``).
   * - 405 Method Not Allowed
     - When the HTTP method is not allowed.
   * - 429 Too Many Requests
     - When the per-minute request limit is exceeded.
   * - 500 Internal Server Error
     - When an internal server error occurs.

Table: Error Response
