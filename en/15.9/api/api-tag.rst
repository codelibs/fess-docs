========
Tags API
========

This document describes the v2 Tags API of |Fess|, with which logged-in users manage their own
tags and put them on documents.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   Tags are disabled by default. To use them, set ``user.tag.enabled=true`` in
   ``fess_config.properties``. ``features.user_tag`` of ``/api/v2/ui/config`` reports the state.
   While tags are disabled, a request that passes the CSRF and Origin checks and uses a
   supported method gets ``invalid_request`` (400) from the tag endpoints.

How Tags Work
=============

- Tags are kept per user. The user who creates a tag owns it, and the owner is the login user ID.
  Two users can use the same name and still have two separate tags.
- Only logged-in users can use tags. Every tag endpoint acts as the user of the login session; an
  access token does not stand in for a login. A caller without a login gets ``auth_required``
  (401).
- A new tag is private: only its owner sees it. When the owner shares the tag, every logged-in
  user can see it and filter by it. A user who is not logged in sees no tag, shared or not.
- Only the owner can change or delete a tag, or put it on and take it off documents. A shared tag of
  another user can only be shown and filtered on. Administrators manage all tags on the admin
  screen (see :doc:`../admin/tagtype-guide`).
- A tag is put on the URL of a document, so every indexed document with that URL gets it.

Each tag has two identifiers.

``value``
    The tag value, ``base64url(name):base64url(owner)`` (UTF-8, without padding), stored in the
    ``tag`` field of the index. Treat it as an opaque value to filter search results with.

``id``
    The tag ID, the SHA-256 of ``value`` in lowercase hex (64 characters). It goes into paths such
    as ``/api/v2/tags/{tagId}``. Renaming a tag changes both ``value`` and ``id``.

A tag name is NFKC-normalized, runs of whitespace are collapsed to one space and the ends are
trimmed. The result must be 1 to ``user.tag.name.max.length`` (default: ``50``) characters, and
names with a control or format character (such as a zero-width character or a bidi override) are
refused.

Tags in Search
==============

While ``user.tag.enabled`` is ``true``, the search API (``/api/v2/search``) handles tags as follows.

- Each hit carries the tags that the caller can see as ``tags``. Each entry has ``value``,
  ``name``, ``owner``, ``mine`` (``true`` when the caller owns the tag) and ``shared`` (``true``
  for a shared tag). ``tags`` is absent when there is none. The ``tag`` index field itself is never
  returned.
- ``facet.field=tag`` returns in ``facet_field`` a facet of the tags that the caller can see. Besides
  ``value`` and ``count``, each bucket has ``label`` (the tag name), ``owner``, ``mine`` and
  ``shared``.
- ``fields.tag=<value>`` narrows the results to the documents with a tag. Pass the ``value`` of a
  hit's ``tags`` or of a facet bucket as is.

A condition on tags (``fields.tag``, ``tag:``, ``ex_q``, ``facet.query``) matches only an exact
value of a tag that the caller can see. The value of a tag the caller cannot see, and wildcard,
prefix, fuzzy and range conditions, match nothing. A caller without a login gets no tags and no tag
facet, and a tag condition matches nothing.

One user sees at most ``user.tag.visible.max.size`` (default: ``1000``) tags, the user's own tags
first. Tags beyond that do not appear in ``tags`` of the hits or in the facet, but can still be
filtered on.

When Documents Reflect Changes
==============================

Creating, changing and deleting tags, and putting them on and taking them off documents, show in the
tag endpoints at once. The ``tag`` field of the indexed documents, however, is updated through an
in-memory queue that the "Log Aggregator" job (``log_aggregator``) applies in bulk every minute. The
search hits, the facet and the filters therefore reflect a change after up to about a minute. After
a rename, the documents keep the old value until the queue is next processed, and the tag does not
show on them in the meantime.

For the queue and the jobs, see :doc:`../admin/tagtype-guide`.

Listing Tags
============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/tags``
==================  ====================================================

Returns the tags that the caller owns, by sort order and name. Shared tags of other users are not
included.

Response
--------

On success (200), the following fields are returned directly under ``response`` of the common envelope.

::

    {
      "response": {
        "status": 0,
        "tags": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "value": "dG8tcmV2aWV3:YWxpY2U",
            "name": "to-review",
            "shared": false,
            "sort_order": 0,
            "path_count": 3
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``tags``
     - The caller's tags. Each has ``id``, ``value``, ``name``, ``shared`` (``true`` for a shared
       tag), ``sort_order`` and ``path_count`` (the number of URLs the tag is on).

Table: Response Fields

Creating a Tag
==============

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/tags``
==================  ====================================================

Creates a tag of the caller. As a state-changing request, it requires the ``X-Fess-CSRF-Token``
header (see :doc:`api-overview`).

- A user can have at most ``user.tag.max.tags`` (default: ``1000``) tags. Beyond that, the
  endpoint answers ``invalid_request`` (400).
- When the caller already has a tag of the name, the endpoint answers ``conflict`` (409). Another
  user having a tag of the same name does not matter.

Send ``Content-Type: application/json``; the body can be at most 1 KiB (1024 bytes).

::

    {
      "name": "to-review",
      "shared": false
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Body

   * - ``name``
     - Tag name (str, required).
   * - ``shared``
     - ``true`` lets every logged-in user see the tag (bool, default: ``false``).

Table: Request Body

Response
--------

On success (200), ``tag`` directly under ``response`` holds the new tag, in the form of an entry of
``GET /api/v2/tags`` with a ``path_count`` of ``0``.

Changing a Tag
==============

Request
-------

==================  ====================================================
HTTP Method         PUT
Endpoint            ``/api/v2/tags/{tagId}``
==================  ====================================================

Renames a tag of the caller or changes whether it is shared. The ``X-Fess-CSRF-Token`` header is
required.

- The body has ``name``, ``shared`` or both.
- A new ``name`` renames the tag, which gives it a new ``id`` and ``value``. The documents with the
  old value get the new one when the queue is next processed. Renaming to a name the caller already
  uses answers ``conflict`` (409) and leaves the tag unchanged.
- ``shared`` only changes who sees the tag; no document is updated. Setting ``shared`` to ``false``
  keeps the roles and groups an administrator added to the permissions.
- A shared tag of another user answers ``forbidden`` (403), and a tag the caller cannot see
  ``not_found`` (404).
- A write that keeps losing a race with another update also answers ``conflict`` (409).

::

    {
      "name": "reviewed",
      "shared": true
    }

On success (200), ``response`` holds ``tag`` (the tag as changed) and ``renamed`` (``true`` when the
tag was renamed, in which case ``tag.id`` and ``tag.value`` are new).

Deleting a Tag
==============

Request
-------

==================  ====================================================
HTTP Method         DELETE
Endpoint            ``/api/v2/tags/{tagId}``
==================  ====================================================

Deletes a tag of the caller. The documents lose its value when the queue is next processed. The
``X-Fess-CSRF-Token`` header is required. A shared tag of another user answers ``forbidden`` (403),
and a tag the caller cannot see ``not_found`` (404).

On success (200), ``response`` holds ``id`` (the deleted tag ID) and ``deleted`` (always ``true``).

Getting the Tags of a Document
==============================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Returns the tags on the document's URL that the caller can see, and the caller's own tags that are
not on it. The document is looked up with the caller's roles, so a document the caller cannot
search answers ``not_found`` (404).

Response
--------

On success (200), the following fields are returned directly under ``response`` of the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "tags": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "value": "dG8tcmV2aWV3:YWxpY2U",
            "name": "to-review",
            "owner": "alice",
            "mine": true,
            "shared": false
          },
          {
            "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
            "value": "c3BlY3M:Ym9i",
            "name": "specs",
            "owner": "bob",
            "mine": false,
            "shared": true
          }
        ],
        "addable": []
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``doc_id``
     - Document ID (str).
   * - ``tags``
     - The tags on the document's URL that the caller can see. Each has ``id``, ``value``,
       ``name``, ``owner``, ``mine`` (``true`` when the caller owns the tag) and ``shared``
       (``true`` for a shared tag).
   * - ``addable``
     - The caller's tags that are not on the document's URL, in the same form as ``tags``.
   * - ``added``
     - POST only. ``false`` when the tag was already on the document (bool).
   * - ``tag``
     - POST only. The tag put on the document, in the same form as ``tags``.
   * - ``removed``
     - DELETE only. ``false`` when the tag was not on the document (bool).

Table: Response Fields

Putting a Tag on a Document
===========================

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Adds the document's URL to a tag of the caller. The ``X-Fess-CSRF-Token`` header is required.

The body (``Content-Type: application/json``, at most 1 KiB) gives either ``id``, an existing tag,
or ``name``, a tag name. When both are given, ``id`` wins.

::

    {
      "name": "to-review"
    }

- With ``name``, a private tag of the name is created and put on the document when the caller has
  none. The new tag counts against ``user.tag.max.tags``.
- A tag can be on at most ``user.tag.max.paths`` (default: ``10000``) URLs. Beyond that, the
  endpoint answers ``invalid_request`` (400).
- An ``id`` of another user's tag answers ``forbidden`` (403) when the caller can see the tag and
  ``not_found`` (404) otherwise.
- On success, the response has the fields of Getting the Tags of a Document plus ``added`` and
  ``tag``. The tag endpoints show the tag at once; the search results of the documents with the URL
  reflect it when the queue is next processed (about a minute later).

Taking a Tag off a Document
===========================

Request
-------

==================  ====================================================
HTTP Method         DELETE
Endpoint            ``/api/v2/documents/{docId}/tags/{tagId}``
==================  ====================================================

Removes the document's URL from the caller's tag given by ``tagId``. The ``X-Fess-CSRF-Token``
header is required. Another user's tag answers ``forbidden`` (403) when the caller can see it and
``not_found`` (404) otherwise. On success, the response has the fields of Getting the Tags of a
Document plus ``removed``.

Error Response
==============

For details on the error model, see :doc:`api-overview`. The tag endpoints return the following
HTTP statuses.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - When the request is invalid, including when tags are disabled, the tag name is invalid, a
       required field is missing, or ``user.tag.max.tags`` or ``user.tag.max.paths`` would be
       exceeded.
   * - 401 Unauthorized
     - Without a login (an access token does not stand in for one).
   * - 403 Forbidden
     - A missing or expired CSRF token, or a change to another user's tag. The CSRF check comes
       before the login check, so a state-changing request without a session gets 403, not 401.
   * - 404 Not Found
     - When the tag does not exist or the caller cannot see it, or the document is not found or the
       caller cannot search it.
   * - 405 Method Not Allowed
     - When the HTTP method is not allowed.
   * - 409 Conflict
     - When a tag of the name already exists, or a write lost a race with another update.
   * - 413 Payload Too Large
     - When the request body exceeds the size limit (1 KiB).
   * - 415 Unsupported Media Type
     - When the ``Content-Type`` is not supported.
   * - 500 Internal Server Error
     - When an internal server error occurs.

Table: Error Response

Settings
========

The following settings in ``fess_config.properties`` adjust tags.

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - Property
     - Description
     - Default
   * - ``user.tag.enabled``
     - Whether logged-in users can use tags.
     - ``false``
   * - ``user.tag.name.max.length``
     - Maximum length of a tag name, in code points.
     - ``50``
   * - ``user.tag.max.tags``
     - Maximum number of tags one user can own.
     - ``1000``
   * - ``user.tag.max.paths``
     - Maximum number of URLs one tag can be put on.
     - ``10000``
   * - ``user.tag.queue.max.size``
     - Maximum number of changes held in memory until they reach the documents. A change beyond it
       is dropped with a WARN log.
     - ``10000``
   * - ``user.tag.process.batch.size``
     - Number of URLs updated per bulk request when changes are applied to the documents.
     - ``100``
   * - ``user.tag.visible.max.size``
     - Maximum number of tags visible to one user in a search.
     - ``1000``
