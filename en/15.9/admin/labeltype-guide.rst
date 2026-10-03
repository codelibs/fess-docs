=====
Label
=====

Overview
========

This page explains the configuration settings related to labels.
Labels can classify documents displayed in search results.
Label configuration specifies the paths to apply labels using regular expressions.
When labels are registered, a label pull-down box is displayed in the search options.

The label settings here apply to web or file system crawl configurations.

Management Operations
=====================

Display Method
--------------

To open the label configuration list page shown below, click [Crawler > Label] in the left menu.

|image0|

Click the configuration name to edit it.

Creating Configuration
----------------------

To open the label configuration page, click the New button.

|image1|

Configuration Items
-------------------

Name
::::

Specifies the name displayed in the label selection pull-down box during searches.

Value
:::::

Specifies the identifier for classifying documents.
Specify using alphanumeric characters.

Included Paths
::::::::::::::

Configures paths to apply labels using regular expressions.
Multiple paths can be specified by writing on multiple lines.
Labels are applied to documents matching the paths specified here.

Excluded Paths
::::::::::::::

Configures paths to exclude from crawl targets using regular expressions.
Multiple paths can be specified by writing on multiple lines.

Permission
::::::::::

Specifies the permission for this configuration.
To display search results to users belonging to the developer group, specify {group}developer.
User-level specification uses {user}username, role-level specification uses {role}rolename, and group-level specification uses {group}groupname.

Virtual Host
::::::::::::

Specifies the virtual host hostname.
For details, refer to :doc:`Virtual Host in the Configuration Guide <../config/security-virtual-host>`.

A search screen accessed through a virtual host shows only the labels whose field names that virtual host.
A label with this field empty is not shown when the search screen is accessed through a virtual host.
An access that matches no virtual host shows all labels, whatever this field holds.

A label can name only one virtual host.
To show the same label on several virtual hosts, create a label with the same name and value for each virtual host, and put that virtual host name in its Virtual Host field.
Because the value is the same, each of those labels narrows the results to the same documents.

Display Order
:::::::::::::

Specifies the display order of labels.

Kind
::::

Specify "Label" or "Tag". An ordinary label is "Label". "Tag" is a tag that users add from the
search screen (see "Tags" below). An existing label without a kind is treated as "Label".


Deleting Configuration
----------------------

Click the configuration name on the list page, then click the Delete button to display a confirmation screen.
Click the Delete button to remove the configuration.

Tags
----

With ``user.tag.enabled=true`` (default: ``false``) in ``fess_config.properties``, logged-in users
can tag search results. In the bundled ``bootstrap`` theme, tags are shown on the results, users can
add tags and remove their own, and a "Tags" facet narrows the results. For the API, see
:doc:`../api/api-tag`.

A tag is stored as a label of the kind "Tag": the name is the tag name, the value is the SHA-256 of
the name, the included paths are the tagged URLs (one per line, exact match), and the permissions
decide who can see the tag. A user who adds a tag is added to its permissions.

- A tag is visible only when the permissions of its label match the caller. Administrators can edit
  a tag on this page to share it with a role or a group, or delete it.
- Tags with the same name are merged into one label, so users who added a tag of the same name can
  see where each other's tags are.
- Tags are not included in the label list API (``/api/v2/labels``) or in the label choices of the
  search screen.
- Tags count toward the label limit (``page.labeltype.max.fetch.size``, default: 1000). Once the
  limit is reached, no new tag can be created.
- After an administrator changes or deletes a tag on this page, the indexed documents keep the old
  values until they are crawled again or the "Label Updater" job runs.
- A document can have up to ``user.tag.max.document.tags`` (default: 100) tags, and a tag name can be
  up to ``user.tag.name.max.length`` (default: 50) characters long.

.. |image0| image:: ../../../resources/images/en/15.9/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/labeltype-2.png