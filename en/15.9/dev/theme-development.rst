==================================
Theme Development Guide
==================================

Overview
========

In |Fess| 15.9, the search screen is always a static theme. A static
theme is an independent SPA (Single Page Application) that uses the
``/api/v2/*`` API. Themes are distributed as ZIP files, uploaded
through the admin console, and enabled there. When no theme is
selected, |Fess| uses ``bootstrap``, the static theme bundled with it.

To change how the search screen looks, either install another theme
(see :doc:`../admin/theme-guide`) or make your own: the quickest way
is to copy the bundled theme and change the copy, as described in
`Customizing the Bundled Theme`_.

.. note::

   Static themes are available in |Fess| 15.7 and later, and became the
   default search screen in 15.9. JAR theme plugins, which replaced the
   JSPs of the search screen, were removed in 15.9; see
   `JAR Theme Plugin (Removed in 15.9)`_.

Static Theme
============

A static theme is a collection of static resources that includes a
``theme.yml`` manifest and ``index.html``. Implement the theme itself
as a front-end application that calls the |Fess| ``/api/v2/*`` API.

Structure
---------

A static theme has the following directory structure.

::

    example/
    ├── theme.yml          # Manifest (required)
    ├── index.html         # SPA entry HTML
    ├── assets/            # Static resources such as JavaScript and CSS
    │   └── styles.css
    ├── i18n/              # Localized messages (messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # Help definitions (<locale>.json)
    │   └── en.json
    └── thumbnail.png      # Preview image (optional)

Manifest (theme.yml)
--------------------

``theme.yml`` is a required manifest placed at the root of the ZIP
file. The following is an example of a minimal configuration.

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "15.9.0"
    minFessVersion: "15.9"
    entry: index.html
    spaFallback: true

The fields that can be specified are as follows.

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Field
     - Required
     - Description
   * - ``apiVersion``
     - Required
     - Fixed value ``fess.codelibs.org/v1``.
   * - ``kind``
     - Required
     - Fixed value ``StaticTheme``.
   * - ``name``
     - Required
     - The theme name. Must match ``^[a-z0-9][a-z0-9_-]{0,63}$``. It is
       used for the directory name the theme is expanded into under
       ``themes/`` (when uploading, this is determined automatically
       from ``name``), and for the delivery URL (``/themes/<name>/``).
   * - ``displayName``
     - Required
     - The name displayed in the admin console.
   * - ``version``
     - Required
     - Semantic versioning format (e.g., ``15.9.0``, ``15.9.1-beta.1``). By convention the
       ``major.minor`` is the |Fess| line the theme targets, so that the version alone answers
       which |Fess| a theme is for.
   * - ``author``
     - Optional
     - The author's name.
   * - ``description``
     - Optional
     - A description of the theme.
   * - ``license``
     - Optional
     - The license.
   * - ``homepage``
     - Optional
     - The homepage URL.
   * - ``minFessVersion``
     - Optional
     - The minimum |Fess| version the theme supports. Keep it equal to the ``major.minor`` of
       ``version``. There is no ``maxFessVersion``: see `Publishing`_.
   * - ``supportedLocales``
     - Optional
     - A list of supported locales (e.g., ``[en, ja, de]``).
   * - ``entry``
     - Optional
     - The SPA entry HTML. Defaults to ``index.html``.
   * - ``spaFallback``
     - Optional
     - Deprecated. Accepted for compatibility but no longer read: since
       15.9 the entry HTML is always served for the search screen paths.

.. note::

   When uploading via ZIP, the destination directory name is
   determined automatically from ``name``. If you place a theme
   manually in the ``themes/`` directory, make sure the directory name
   matches ``name``. Themes whose directory name does not match are
   ignored on rescan.

.. note::

   The preview thumbnail is placed at the root of the theme with the
   fixed name ``thumbnail.png`` (it is displayed in the theme list in
   the admin console). This image is recognized by its file name, not
   by a manifest field. A size of 512KB or less and 512x512 pixels or
   less is recommended.

Serving and API
---------------

- A static theme is served under ``/themes/<name>/`` (``<name>`` is
  the ``name`` in ``theme.yml``).
- The entry HTML (``index.html`` by default) is returned for the paths
  ``/``, ``/search``, ``/advance``, ``/help``, ``/error``, ``/profile``,
  ``/cache``, and ``/chat``, and subsequent routing is handled by the
  SPA. Since 15.9 this happens whatever ``spaFallback`` says; the field
  is no longer read.
- Errors are rendered by the theme as well: when a request fails, a
  browser receives the theme's entry HTML at the requested URL, with the
  real HTTP status.
- The admin console (``/admin/*``), ``/api/*``, the login screen, and
  similar are not covered by the static theme and are handled by the
  |Fess| core.
- ``{{themePath}}`` in the entry HTML is replaced with ``themes/<name>``
  when the page is served. Refer to the theme's own files from
  ``index.html`` as ``{{themePath}}/assets/styles.css`` and so on. The
  theme name is then not written into the page, so the theme loads its
  own files under whatever name it is installed.
- The entry HTML is served with a ``Content-Security-Policy`` header that
  allows scripts, styles, images and connections only from |Fess|
  itself (inline styles are allowed; inline scripts are not). Fonts or
  scripts from an external CDN are therefore not loaded; ship them in the
  theme.
- The ``Content-Security-Policy`` of the entry HTML contains
  ``frame-ancestors 'none'``, and the response also carries
  ``X-Frame-Options: DENY``, so the page is not shown in a frame of
  another page. The ``frame-ancestors`` value can be changed with
  ``theme.index.frame.ancestors`` in ``fess_config.properties``
  (default: ``'none'``). An empty value drops ``frame-ancestors``
  (``X-Frame-Options: DENY`` is still sent). Under
  ``frame-ancestors 'none'``, WebKit-based browsers such as Safari leave
  blank the frames that a theme shows from a ``blob:`` URL (a PDF
  preview or a cached copy). Set the value to empty to show them.
- The theme's SPA retrieves data such as search results and chat from
  the ``/api/v2/*`` API.

Packaging
---------

Using ``scripts/package.sh`` from the
`fess-themes <https://github.com/codelibs/fess-themes>`__ repository,
you can package a theme into a ZIP for distribution.

::

    ./scripts/package.sh example

``dist/example-<version>.zip`` is generated (``<version>`` is the
``version`` in ``theme.yml``).

.. note::

   ``theme.yml`` must be placed at the root of the ZIP. If it is
   placed in a subdirectory, it will not be recognized when uploaded.

Publishing
----------

The themes the |Fess| project develops are published under
https://maven.codelibs.org/release/org/codelibs/fess/themes/ , at
``<name>/<version>/<name>-<version>.zip`` with a ``.sha1`` beside it, and a per-theme
``maven-metadata.xml`` listing the published versions. ``bin/fess-setup install theme <name>``
reads that metadata to pick the version built for the running |Fess|.

Version a theme on the |Fess| line it targets and raise the version whenever you change what the
archive ships. A published version is never overwritten, so a change that keeps its version is
simply never distributed.

This is also why there is no upper-bound field in the manifest. Because a published archive never
changes, an upper bound could not be added later for a theme that stops working on a newer |Fess|.
Not publishing that theme for the newer line says the same thing, at the point it is known.

.. note::

   Enumerate the published versions from ``maven-metadata.xml`` rather than from a directory
   listing. The directory index is generated periodically, so a newly published theme is readable
   through its metadata before it appears in any listing.

Installation and Activation
----------------------------

1. In the admin console, open "System" -> "Theme" (``/admin/theme/``).
2. Upload the ZIP file you created. A published theme can instead be installed from the command
   line with ``bin/fess-setup install theme <name>``; see :doc:`../install/fess-setup`.
3. On the list page, select the target theme from the "Default Theme"
   drop-down and click the "Set" button to enable it.

The activation mechanism works as follows.

- Clicking "Set" saves the selected theme name to the
  ``theme.default`` system property, making it the system-wide default
  theme.
- If you match the theme name to a virtual host key, the theme is
  applied only when that virtual host is accessed. This lets you
  switch themes per virtual host.
- If you update the ``themes/`` directory on disk directly, you can
  rescan it with "Reload".

.. note::

   There are limits on ZIP uploads, such as file size, total size
   after extraction, and number of entries, which can be adjusted with
   the ``theme.*`` properties in ``fess_config.properties`` (for
   example, ``theme.upload.max.size`` defaults to 50MB, and
   ``theme.directory.path`` defaults to ``themes``). During extraction,
   validation is performed to prevent ZIP Slip and zip bomb attacks.

.. _theme-customize-bundled:

Customizing the Bundled Theme
-----------------------------

The bundled theme ``bootstrap`` is in ``app/themes/bootstrap/`` of the
|Fess| installation (``/usr/share/fess/app/themes/bootstrap/`` for the
RPM/DEB packages). Do not edit it in place: an upgrade replaces it, and
the name ``bootstrap`` is reserved for it, so it can be neither deleted
nor replaced by an upload. Copy it under a new name instead.

1. Copy the directory, for example to ``mytheme``::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. In ``theme.yml``, change ``name`` to ``mytheme`` and change
   ``displayName``. ``name`` must match the directory name.

3. Leave ``index.html`` as it is. The bundled ``index.html`` refers to
   its own files, such as the stylesheet, the logos and the script, as
   ``{{themePath}}/assets/...``, and |Fess| replaces ``{{themePath}}``
   with ``themes/<name>`` (the ``name`` in ``theme.yml``) when it serves
   the page. Renaming the copy is therefore enough for it to load its own
   files. When you add a file that ``index.html`` refers to, write its
   URL as ``{{themePath}}/assets/...`` as well.

4. Make your changes:

   - Colors and layout: ``assets/styles.css``.
   - Logos: ``assets/logo-head.png`` (header) and ``assets/logo.png``
     (search top page).
   - Texts, such as the footer (``footer.copyright_org``): the
     ``i18n/messages.<locale>.json`` files, one per language.
   - Page structure: ``index.html``.

5. Package the directory as a ZIP with ``theme.yml`` at its root, and
   upload it on "System" > "Theme" in the admin console::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   Alternatively, place the directory in ``app/themes/`` and click
   "Reload" on the same page.

6. Select ``mytheme`` as the default theme on that page.

.. note::

   Replace the copy with a fresh one from the bundled theme after each
   |Fess| upgrade and reapply your changes, as the bundled theme follows
   the ``/api/v2/*`` API of its |Fess| version.

JAR Theme Plugin (Removed in 15.9)
==================================

The JAR theme plugin type, which put JSPs, CSS and images in a ``fess-theme-*`` JAR and
applied them as the theme named after a virtual host key, was removed in |Fess| 15.9.
15.9 does not extract a JAR theme and does not use it for any screen.

- Installing one from "System" > "Plugin" in the admin UI only places it in
  ``app/WEB-INF/plugin/`` as a generic JAR of type ``jar``; no screen changes. A
  ``fess-theme-*.jar`` left over from an earlier version is listed the same way, and can be
  deleted on that page or with ``bin/fess-setup remove plugin <name>``.
- ``bin/fess-setup`` neither lists nor installs ``fess-theme-*``.

Move the changes you made in a JAR theme to a static theme:

- For the colors, layout and logo of the search screen, copy the bundled theme and change
  the copy (see `Customizing the Bundled Theme`_).
- If you changed the look per virtual host, install a static theme named after the
  virtual host (see :doc:`../config/security-virtual-host`).
- The login screen (``/login/``) is the same for every virtual host. A theme cannot
  change it.

Examples of Existing Themes
============================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - A
  collection of static themes (includes multiple static themes such as
  ``codesearch`` and ``docsearch``)

Reference
=========

- :doc:`plugin-architecture` - Plugin architecture
- :doc:`../admin/plugin-guide` - Plugin installation
