===
Tag
===

Overview
========

This page explains the screen that manages the tags of users.

A tag is a marker that a logged-in user puts on documents in the search results. Tags are kept per
user: the user who creates a tag owns it, and two users can use the same name and still have two
separate tags. Tags are not :doc:`labels <labeltype-guide>`, which administrators define by URL
patterns; users create tags themselves and put them on individual documents.

Tags are disabled by default. To use them, set ``user.tag.enabled=true`` in
``fess_config.properties``. Once they are enabled, the bundled ``bootstrap`` theme lets logged-in
users put tags on search results and take them off, and filter by a tag facet. "My tags" lets them
rename, share and delete their own tags. Shared tags of other users are shown with a "Shared:"
prefix. For the user API and the settings, see :doc:`../api/api-tag`.

On this screen, administrators list, create, edit and delete the tags of every user.

Management Operations
=====================

Display Method
--------------

To open the tag list page, click [Crawler > Tag] in the left menu. Viewing requires the
``admin-tagtype`` or ``admin-tagtype-view`` role; creating, editing and deleting require
``admin-tagtype``.

The list shows the name and the owner of each tag, by sort order, name and owner. You can search by
name and by owner; each matches the tags that contain the text entered.

Click a name to edit the tag.

Creating Configuration
----------------------

To open the tag creation page, click the New button.

Configuration Items
-------------------

Name
::::

Specifies the tag name. The name is NFKC-normalized, runs of whitespace are collapsed to one space
and the ends are trimmed. The result must be 1 to ``user.tag.name.max.length`` (default: 50)
characters and cannot contain a control or format character.

Owner
:::::

Specifies the login user ID of the user who owns the tag. The owner and the name together identify
a tag, so one owner cannot have two tags of the same name, even on different virtual hosts.

When you change the owner, the user permission of the old owner in Permissions is replaced with
that of the new owner.

Paths
:::::

Specifies the URLs of the documents to put the tag on, one per line. A URL must equal the ``url``
field of an indexed document; regular expressions are not used. A tag can have at most
``user.tag.max.paths`` (default: 10000) URLs.

Permissions
:::::::::::

Specifies the users, groups and roles that can see the tag, as for labels: {user}user name for a
user, {group}group name for a group and {role}role name for a role. When left empty, only the owner
can see the tag.

The owner always sees their own tags, whatever the permissions. A user who is not logged in never
sees a tag, whatever the permissions.

Virtual Host
::::::::::::

Specifies the host name of the virtual host where the tag is shown. A tag created by a user gets
the virtual host the user was accessing. On a search screen accessed through a virtual host, only
the tags with that virtual host name here are visible. An access that matches no virtual host sees
tags whatever this field holds. For details, see
:doc:`Virtual Host in the Configuration Guide <../config/security-virtual-host>`.

Sort Order
::::::::::

Specifies the display order of the tag.

Deleting Configuration
----------------------

Click a name on the list page and then the Delete button to show a confirmation screen. Clicking
the Delete button deletes the tag, and its value is removed from the documents.

Sharing
=======

When a user shares a tag, the values of ``role.search.guest.permissions`` (default:
``{role}guest``) are added to its permissions. Whether a tag is visible is decided with these values
added to the roles of the logged-in user, so a shared tag is visible to every logged-in user, who
can also filter by it. Unsharing removes only these values.

On this screen, an administrator can also add groups or roles to the permissions to show a tag to
some users only. Only the owner and administrators can change a tag; other users can only show and
filter by the tags they see.

How Changes Reach Documents
===========================

A document keeps its tags in the ``tag`` field of the index, as ``base64url(name):base64url(owner)``.

- Creating, editing and deleting tags, and users putting tags on and taking them off documents, are
  saved to the tags (the ``fess_config.tag_type`` index) at once. The documents are updated through
  an in-memory queue that the "Log Aggregator" job (``log_aggregator``) applies in bulk every
  minute, so the search results reflect a change after up to about a minute.
- Changing the paths on this screen updates the documents of the added and removed URLs. Changing
  the name or the owner replaces the old value on the documents with the new one.
- When documents are indexed by a crawl or a data store, their ``tag`` field is set from the paths
  of the tags, so tags survive a re-crawl.
- The "Tag Updater" job (``tag_updater``) rebuilds the ``tag`` field of every document from the
  tags. It has no schedule; run it from the scheduler when needed.

Notes for Operators
===================

- **Run Log Aggregator on every node.** Each JVM has its own queue, which only the Log Aggregator of
  that node processes. Keep the target of the ``log_aggregator`` job at the default ``all``; when
  it is limited to some nodes, the changes received by the other nodes never reach the documents.
- **Run Tag Updater in the following cases.** The queue is in memory, so changes not yet applied are
  lost when |Fess| restarts. While ``user.tag.enabled=false``, tag changes do not reach the
  documents, and a re-crawl clears their ``tag`` field. After a restore from a backup, the tags of
  the documents also need rebuilding. And when the queue exceeds ``user.tag.queue.max.size``
  (default: 10000), the changes beyond it are dropped with a WARN log. In each case, running
  ``tag_updater`` rebuilds the tags of the documents.
- **The owner of a tag is the login user ID.** When a user ID changes, the tags stay with the old
  ID. With SAML, the NameID must be persistent. With Entra ID the owner is the UPN, and with LDAP it
  is the user name with the letter case typed at login. Deleting a user leaves the user's tags;
  delete the ones no longer needed on this screen.
- **Existing indexes work too.** At startup, when the document index has no mapping for the
  ``tag`` field, it is added as ``keyword``. Existing fields are not changed.
- The tags are stored in the ``fess_config.tag_type`` index. They are included in ``fess_config.bulk``
  of a backup, but not in ``fess_basic_config.bulk``.
