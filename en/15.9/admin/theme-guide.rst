=====
Theme
=====

Overview
========

The Theme feature manages "static themes" — a bundled set of static assets (HTML / CSS / JavaScript, etc.) that define the appearance of the search interface. A static theme is uploaded as a ZIP archive and extracted into the theme directory on the server (default: ``themes``, configurable via ``theme.directory.path``). Each theme root must contain a ``theme.yml`` manifest that describes the theme's metadata.

.. note::
   JSP-based themes are managed through Plugin Management and are outside the scope of this page.
   The ``admin-theme`` role is required to perform operations on this page (the ``admin-theme-view`` role is sufficient for read-only access).

Obtaining a Theme
=================

The themes developed by the |Fess| project are published as ZIP archives under
https://maven.codelibs.org/release/org/codelibs/fess/themes/ , at
``<name>/<version>/<name>-<version>.zip`` with a ``.sha1`` checksum beside each one.

A theme's version states the |Fess| line it targets: ``15.9.0`` is a theme for |Fess| 15.9, and
its ``minFessVersion`` says the same. There is no upper-bound field. A published archive never
changes, so an upper bound could not be added afterwards for a theme that stops working on a later
|Fess|; that a theme is not published for a line says the same thing, at the point it is known.

There are two ways to install one.

* ``bin/fess-setup install theme <name>`` downloads the theme built for this |Fess|, checks it
  against the published checksum and installs it. See :doc:`../install/fess-setup`.
* Download the ZIP and upload it on this page, as described in `Uploading a Theme`_ below.

A theme can also be packaged from a checkout of the
`fess-themes <https://github.com/codelibs/fess-themes>`__ repository, which always matches the
source you are looking at; see :doc:`../dev/theme-development`.

Management Operations
=====================

Display Method
--------------

To open the registered theme list page shown below, click [System > Theme] in the left menu.

Theme List
----------

The list page displays the static themes registered in the theme directory. The columns shown for each entry are as follows.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Thumbnail
     - Displays ``thumbnail.png`` located in the theme directory. Not shown if the file does not exist.
   * - Name
     - The theme name (the theme's directory name). Click to open the details page.
   * - Display Name
     - The ``displayName`` field from the manifest.
   * - Version
     - The ``version`` field from the manifest.
   * - Default
     - A check mark is shown when the theme is set as the default theme.
   * - Actions
     - A Delete button is shown to remove the theme (not shown for the default theme).

Table: Theme List Columns


Setting the Default Theme
--------------------------

Select a theme from the pull-down menu at the top of the list page and click the [Set Default] button to set the default theme applied to the search interface. Selecting [(no default)] and clicking [Set Default] clears the default theme assignment. After saving, the theme information is reloaded and the change takes effect immediately.


Uploading a Theme
-----------------

Click the [Upload] button to open the upload page. Select a theme ZIP file and click the [Upload] button to install the theme.

* Only ``.zip`` archives can be uploaded.
* The maximum upload size is 50 MB by default (``theme.upload.max.size``).
* The ZIP archive must contain a ``theme.yml`` manifest at its root.

If a theme with the same name already exists, it is replaced. The replaced theme is retained as a backup for a fixed period (default 7 days, ``theme.upload.attic.retention.days``).

If the uploaded archive fails manifest validation, or if the extracted size, entry count, or compression ratio exceeds the server limits (zip bomb protection), the installation is rejected and an error message is displayed.


theme.yml Manifest
------------------

Place a ``theme.yml`` file (YAML format) at the root of the static theme to describe the theme's metadata. The available fields are as follows.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|
.. list-table::
   :header-rows: 1

   * - Field
     - Required
     - Description
   * - ``apiVersion``
     - Required
     - Specify ``fess.codelibs.org/v1``.
   * - ``kind``
     - Required
     - Specify ``StaticTheme``.
   * - ``name``
     - Required
     - The theme name. Must match the pattern ``^[a-z0-9][a-z0-9_-]{0,63}$`` and must match the theme's directory name.
   * - ``displayName``
     - Required
     - The name displayed on screen (up to 4096 characters).
   * - ``version``
     - Required
     - The version in SemVer format (e.g. ``1.0.0``).
   * - ``author``
     - Optional
     - The author.
   * - ``description``
     - Optional
     - A description.
   * - ``license``
     - Optional
     - The license.
   * - ``homepage``
     - Optional
     - The homepage URL.
   * - ``minFessVersion``
     - Optional
     - The minimum |Fess| version supported by this theme.
   * - ``supportedLocales``
     - Optional
     - The locales supported by this theme.
   * - ``entry``
     - Optional
     - The entry point file (default: ``index.html``).
   * - ``spaFallback``
     - Optional
     - Enables or disables SPA-style fallback (default: ``true``).

Table: theme.yml Fields


Deleting a Theme
----------------

A theme can be deleted using the Delete button on the list page or the [Delete] button on the details page. A theme that is set as the default theme cannot be deleted. Clear the default theme assignment before deleting. Deleted themes are retained as a backup for a fixed period (default 7 days, ``theme.upload.attic.retention.days``).


Reload
------

If you have edited the theme directory directly on the server, click the [Reload] button to reload the theme information from disk into memory.


Theme Details
-------------

Click a theme name on the list page to open the details page. The details page shows the manifest contents (name, display name, version, default status, and health).


Configuration Properties
=========================

The main configuration settings for the Theme feature can be changed in ``fess_config.properties``.

.. tabularcolumns:: |p{6cm}|p{3cm}|p{5cm}|
.. list-table::
   :header-rows: 1

   * - Property
     - Default
     - Description
   * - ``theme.directory.path``
     - ``themes``
     - The directory used to store themes (relative to the servlet context, or an absolute path).
   * - ``theme.upload.max.size``
     - ``52428800``
     - The maximum ZIP upload size in bytes (approximately 50 MB).
   * - ``theme.upload.max.extracted.size``
     - ``209715200``
     - The maximum total size after extraction in bytes (approximately 200 MB).
   * - ``theme.upload.max.entries``
     - ``1000``
     - The maximum number of entries allowed in the ZIP.
   * - ``theme.upload.max.compression.ratio``
     - ``100``
     - The maximum compression ratio per entry.
   * - ``theme.upload.zip.ratio.max``
     - ``50``
     - The cumulative compression ratio limit (zip bomb protection).
   * - ``theme.upload.zip.ratio.check.threshold.bytes``
     - ``65536``
     - The number of compressed bytes at which cumulative compression ratio evaluation begins.
   * - ``theme.upload.attic.retention.days``
     - ``7``
     - The number of days to retain backups of replaced or deleted themes.

Table: Theme Configuration Properties
