===========
TagType API
===========

Overview
========

TagType API is an API for managing the tags of users in |Fess|, the per-user tags that logged-in users
put on documents (see :doc:`../../admin/tagtype-guide`). It manages the tags of every user, whether
``user.tag.enabled`` is ``true`` or not.

For common specifications regarding authentication, responses (``status`` codes, ``version`` field,
error format, HTTP status codes, etc.), refer to :doc:`api-admin-overview`.
To access this API, you must provide an access token with admin API permission (``admin-api``)
in the ``Authorization: Bearer <access_token>`` header.

The JSON field names of this API are snake_case (``sort_order``, ``virtual_host``, ``seq_no``,
``primary_term``, ...).

Base URL
========

::

    /api/admin/tagtype

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /settings
     - List tags
   * - GET
     - /setting/{id}
     - Get a tag
   * - POST
     - /setting
     - Create a tag
   * - PUT
     - /setting
     - Update a tag
   * - DELETE
     - /setting/{id}
     - Delete a tag

List Tags
=========

Request
-------

::

    GET /api/admin/tagtype/settings

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``size``
     - Integer
     - No
     - Number of items per page. Default is the ``paging.page.size`` setting value (``25`` by default).
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1). Default is ``1``.
   * - ``name``
     - String
     - No
     - Filter by tag name (wildcard search: matches the names that contain the text).
   * - ``owner``
     - String
     - No
     - Filter by owner (wildcard search: matches the owners that contain the text).

The tags are sorted by sort order, name and owner.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   The list leaves out the paths of the tags, which can be long, so the entries have no ``paths``.
   PUT replaces the whole tag: to edit a tag, get it with ``GET /setting/{id}`` first so that its
   ``paths`` are kept.

Get a Tag
=========

Request
-------

::

    GET /api/admin/tagtype/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` and ``primary_term`` identify the version of the tag that was read. ``paths`` and
``permissions`` hold one entry per line.

Create a Tag
============

Request
-------

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

Field Descriptions
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Field
     - Type
     - Required
     - Description
   * - ``name``
     - String
     - Yes
     - Tag name. It is NFKC-normalized, runs of whitespace are collapsed and the ends are trimmed;
       the result must be 1 to ``user.tag.name.max.length`` (default: ``50``) characters without a
       control or format character.
   * - ``owner``
     - String
     - Yes
     - Login user ID of the user who owns the tag (max 1000 characters).
   * - ``paths``
     - String
     - No
     - URLs of the documents to put the tag on, separated by a newline (``\n``). Each must equal the
       ``url`` field of a document. At most ``user.tag.max.paths`` (default: ``10000``).
   * - ``permissions``
     - String
     - No
     - Users/groups/roles that can see the tag (e.g. ``{role}guest``), separated by a newline
       (``\n``). When empty, only the owner can see the tag. ``{role}guest`` (the value of
       ``role.search.guest.permissions``) shares the tag with every logged-in user.
   * - ``virtual_host``
     - String
     - No
     - Virtual host (max 1000 characters).
   * - ``sort_order``
     - Integer
     - No
     - Display order (non-negative integer). Defaults to ``0`` if not specified.

The ID of a tag is the SHA-256 of its value, which is made from the name and the owner, so it is
decided by the server. The owner and the name together identify a tag: creating a tag whose owner
already has a tag of the name fails with a validation error (``status: 1``, "A tag with the same
name and owner already exists.").

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

On successful creation, ``created`` is ``true``.

Update a Tag
============

Request
-------

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

The body has all the fields used at creation time, and the following fields in addition. The tag
is replaced as a whole, so send the ``paths`` you want to keep as well.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Field
     - Type
     - Required
     - Description
   * - ``id``
     - String
     - Yes
     - The ID of the tag to update.
   * - ``seq_no``
     - Integer
     - Yes
     - The ``seq_no`` of the tag returned by ``GET /setting/{id}``.
   * - ``primary_term``
     - Integer
     - Yes
     - The ``primary_term`` of the tag returned by ``GET /setting/{id}``.

- When the tag was changed after it was read, that is, ``seq_no`` and ``primary_term`` no longer
  match, the update fails with a validation error (``status: 1``, "The tag was changed by someone
  else. Reload it and try again."). Get the tag again and retry.
- Changing ``name`` or ``owner`` gives the tag a new ID; the response ``id`` is the new one. When the
  owner already has a tag of the new name, the update fails with "A tag with the same name and owner
  already exists.".
- When the owner changes, the user permission of the old owner in ``permissions`` is replaced with
  that of the new owner.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

On update, ``created`` is ``false``.

Delete a Tag
============

Request
-------

::

    DELETE /api/admin/tagtype/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

When the tag is changed while it is being deleted, the deletion fails with "The tag was changed by
someone else. Reload it and try again.".

How Changes Reach Documents
===========================

Creating, updating and deleting a tag through this API is saved to the tags at once. While
``user.tag.enabled`` is ``true``, the change is queued for the documents (the added and removed
paths, a rename or a deletion) and applied by the per-minute "Log Aggregator" job
(``log_aggregator``). While it is ``false``, nothing is queued; run the "Tag Updater" job
(``tag_updater``) after enabling tags. See :doc:`../../admin/tagtype-guide`.

Usage Examples
==============

Share a Tag with Every Logged-in User
-------------------------------------

.. code-block:: bash

    # Read the tag, including paths, seq_no and primary_term
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Send it back with {role}guest added to the permissions
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

List the Tags of a User
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/tagtype/settings" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"owner": "alice", "size": 50, "page": 1}'

See Also
========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../api-tag` - Tags API
- :doc:`../../admin/tagtype-guide` - Tag Management Guide
