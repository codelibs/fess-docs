========
Tags API
========

This document describes the v2 Tags API of |Fess|, which lets users tag documents.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   Tags are disabled by default. To use them, set ``user.tag.enabled=true`` in
   ``fess_config.properties``. ``features.user_tag`` of ``/api/v2/ui/config`` reports the state.

A tag is a label of the kind "Tag" (see :doc:`../admin/labeltype-guide`): the label name is the tag
name, the value is the SHA-256 of the name in hex, the included paths are the tagged URLs, and the
permissions decide who can see the tag. A tag is visible only when its label is visible to the
caller.

The search API (``/api/v2/search``) returns the tags of each hit that the caller can see as
``tags``. ``fields.tag=<value>`` narrows the results to the documents with a tag, and
``facet.field=tag`` returns a tag facet. The ``tag`` index field itself is not returned.

Getting Tags
============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Returns the tags of the document that the caller can see. When the caller cannot search the
document, the endpoint responds with ``not_found`` (404).

Response
--------

On success (200), the following fields are returned directly under ``response`` of the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "addable": true,
        "tags": [
          { "value": "9f86d081884c7d65...", "name": "to-review", "mine": true }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``doc_id``
     - Document ID (str).
   * - ``addable``
     - ``true`` when the caller is logged in and can add tags (bool).
   * - ``added``
     - POST only. ``false`` when the caller had already tagged the document (bool).
   * - ``removed``
     - DELETE only (bool).
   * - ``tags``
     - The tags that the caller can see. Each has ``value`` (the label value, used with
       ``fields.tag``), ``name`` (the tag name) and ``mine`` (``true`` when the caller is in the
       permissions of the tag).

Table: Response Fields

Adding a Tag
============

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Tags the document's URL for the logged-in user; an access token does not stand in for a login. As a
state-changing request, it requires the ``X-Fess-CSRF-Token`` header.

- When a tag of the name exists, the URL is added to its included paths and the user to its
  permissions. Otherwise, a tag that only the user can see is created. Tags with the same name
  therefore merge into one, and users who added a tag of the same name can see where each other's
  tags are.
- Tagging the same document again answers ``added: false``.
- A document can have at most ``user.tag.max.document.tags`` (default: ``100``) tags.

Send ``Content-Type: application/json`` with the tag name in ``name``.

::

    {
      "name": "to-review"
    }

The name is NFKC-normalized, runs of whitespace are collapsed and it is trimmed. It must be 1 to
``user.tag.name.max.length`` (default: ``50``) characters, and names with a control or format
character (such as a zero-width character or a bidi override) are refused.

Removing a Tag
==============

Request
-------

==================  ====================================================
HTTP Method         DELETE
Endpoint            ``/api/v2/documents/{docId}/tags?value=<tag value>``
==================  ====================================================

Removes the logged-in user from the permissions of the tag given by ``value``. When no permission of
a user, a group or a role is left, the tag is deleted and removed from the documents. When the user
is not in the permissions of the tag, the endpoint responds with ``forbidden`` (403). The
``X-Fess-CSRF-Token`` header is required.

Error Response
==============

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - When the request is invalid (including when tags are disabled, the tag name is invalid or a
       tag limit is exceeded).
   * - 401 Unauthorized
     - POST or DELETE without a login.
   * - 403 Forbidden
     - A missing or expired CSRF token, or a DELETE of a tag the user did not add.
   * - 404 Not Found
     - When the document is not found or the caller cannot search it.
   * - 405 Method Not Allowed
     - When the HTTP method is not allowed.
   * - 413 Payload Too Large
     - When the request body exceeds the size limit.
   * - 415 Unsupported Media Type
     - When the ``Content-Type`` is not supported.
   * - 500 Internal Server Error
     - When an internal server error occurs.

Table: Error Response
