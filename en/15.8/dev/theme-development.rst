==================================
Theme Development Guide
==================================

Overview
========

In |Fess|, you can customize the design of the search screen using the
following two methods.

Static Theme
    A mechanism introduced in |Fess| 15.7. Themes are distributed as
    ZIP files, uploaded through the admin console, and enabled there.
    The theme itself is an independent SPA (Single Page Application)
    that uses the ``/api/v2/*`` API and does not depend on the |Fess|
    core's JSP. This approach is recommended when creating a new theme.

JAR Theme Plugin (Legacy)
    A traditional plugin that overrides ``view`` / ``css`` / ``js`` /
    ``images``. It is built as a JAR and installed as a plugin. Use
    this when you want to partially replace existing JSP-based screens.

.. note::

   Static themes are available in |Fess| 15.7 and later. If you are
   targeting 15.6 or earlier, use a JAR theme plugin instead. For how
   to directly edit the search screen's JSP, CSS, and images from the
   admin console, see :doc:`../admin/design-guide`.

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
    version: "1.0.0"
    minFessVersion: "15.7"
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
     - Semantic versioning format (e.g., ``1.0.0``, ``1.2.3-beta.1``).
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
     - The minimum |Fess| version the theme supports.
   * - ``supportedLocales``
     - Optional
     - A list of supported locales (e.g., ``[en, ja, de]``).
   * - ``entry``
     - Optional
     - The SPA entry HTML. Defaults to ``index.html``.
   * - ``spaFallback``
     - Optional
     - Whether the SPA fallback is enabled. Defaults to ``true``.

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
- When ``spaFallback`` is enabled, the entry HTML (``index.html`` by
  default) is returned for the paths ``/``, ``/search``, ``/help``,
  ``/error``, ``/profile``, ``/cache``, and ``/chat``, and subsequent
  routing is handled by the SPA.
- The admin console (``/admin/*``), ``/api/*``, the login screen, and
  similar are not covered by the static theme and are handled by the
  |Fess| core.
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

Installation and Activation
----------------------------

1. In the admin console, open "System" -> "Theme" (``/admin/theme/``).
2. Upload the ZIP file you created.
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

JAR Theme Plugin (Legacy)
=========================

A JAR theme plugin overrides the |Fess| core's ``view`` / ``css`` /
``js`` / ``images`` directories on a per-theme-name basis. For the
general plugin structure and build process, also see
:doc:`plugin-architecture`.

Structure
---------

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # JSP files (search.jsp, index.jsp, header.jsp, etc.)
        ├── css/       # CSS files (style.css, etc.)
        ├── js/        # JavaScript files
        └── images/    # Image files (logo.png, etc.)

.. note::

   Views (templates) are in JSP format. Only the four top-level
   resource directories ``view`` / ``css`` / ``js`` / ``images`` are
   recognized. The artifact name must start with ``fess-theme-``.

pom.xml
-------

The plugin is built as a jar with ``fess-parent`` as the parent POM.
Since a theme consists only of resources, there is usually no need to
declare additional dependencies.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

Customizing CSS and Images
---------------------------

The search screen is built with Bootstrap-based JSPs. You can override
the CSS to change colors and layout, or replace ``images/logo.png`` to
change the logo. For the target class names and markup, check the
actual JSPs (``view/index.jsp``, ``view/search.jsp``, etc.).

Build and Installation
-----------------------

::

    mvn clean package

A JAR file (e.g., ``fess-theme-example-15.8.0.jar``) is generated in
the ``target/`` directory. You can install it from "System" ->
"Plugin" in the admin console. For details on the installation
procedure, see :doc:`../admin/plugin-guide`.

Once installed, each directory in the JAR is expanded to the following
locations, per theme name (the theme name is the artifact name with
the ``fess-theme-`` prefix removed; in the example above, ``example``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Directory in the JAR
     - Expansion destination
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

Activation
----------

A JAR theme is activated using the virtual host feature. If you match
a virtual host key to the theme name, the theme is applied when that
host is accessed.

1. In the virtual host settings under "System" -> "General", map the
   request's ``Host`` header to a theme name (virtual host key), for
   example ``Host:localhost:8080=example``.
2. If needed, also set the same name (``example``) for the virtual
   host in the crawling web configuration, etc.

For details on how to configure virtual hosts, see
:doc:`../admin/general-guide`.

Examples of Existing Themes
============================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - A
  collection of static themes (includes multiple static themes such as
  ``codesearch`` and ``docsearch``)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__ - JAR theme
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__ - JAR theme

Reference
=========

- :doc:`plugin-architecture` - Plugin architecture
- :doc:`../admin/design-guide` - Page Design (direct editing of JSP,
  CSS, and images)
- :doc:`../admin/plugin-guide` - Plugin installation
