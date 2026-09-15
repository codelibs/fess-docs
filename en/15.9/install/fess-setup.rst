==================
fess-setup Command
==================

``bin/fess-setup`` (``bin\fess-setup.bat`` on Windows) is included with the |Fess| ZIP package.
It installs what |Fess| needs but does not bundle: OpenSearch with the plugins |Fess| requires,
Node.js for the Playwright crawler, and |Fess| plugins. It also reports on an installation.

Run it from the |Fess| directory. Without arguments, it prints the list of commands.

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

Exit Codes
==========

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Meaning
   * - ``0``
     - The command succeeded.
   * - ``1``
     - The command failed: for example, a download failed, the requested version does not exist,
       OpenSearch publishes no build for this platform, or ``check`` found a problem.
   * - ``2``
     - The command line is wrong: an unknown command, or a missing argument such as a plugin name.

Installing OpenSearch and Node.js
=================================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>]

Downloads the OpenSearch version this |Fess| supports into ``opensearch/`` in the |Fess| directory,
installs the four plugins |Fess| requires (``opensearch-analysis-fess``,
``opensearch-analysis-extension``, ``opensearch-minhash`` and ``opensearch-configsync``), and
appends the following settings to its ``config/opensearch.yml``:

- ``configsync.config_path``, set to the ``config/dictionary`` directory of that OpenSearch
- ``plugins.security.disabled: true``

A setting that ``opensearch.yml`` already has is not added again, and
``plugins.security.disabled: true`` is not added when the file has any ``plugins.security.*``
setting. When the OpenSearch directory already exists, the download is skipped, so running the
command again on an existing installation only adds the settings that are missing.

The command prints each setting it added, and then whether ``bin/fess.in.sh`` finds this OpenSearch
on its own. It does when this is the only OpenSearch with a ``config/dictionary`` directory under
``opensearch/`` in the |Fess| directory: ``bin/fess.in.sh`` (``bin\fess.in.bat`` on Windows) then
sets ``FESS_DICTIONARY_PATH`` to that directory, and nothing else needs to be configured for an
OpenSearch on the same host. Otherwise the command prints the ``SEARCH_ENGINE_HTTP_URL`` and
``FESS_DICTIONARY_PATH`` values to set, as described in :doc:`install-linux` or
:doc:`install-windows`.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Description
   * - ``--dest <dir>``
     - The directory to extract OpenSearch into, instead of ``opensearch/`` in the |Fess|
       directory. ``bin/fess.in.sh`` does not look for OpenSearch outside that directory.
   * - ``--version <version>``
     - The OpenSearch version to install. The plugins are installed at the same version.

OpenSearch publishes official builds for Linux and Windows only. On other platforms, such as macOS,
the command exits with code ``1`` before downloading anything and suggests installing OpenSearch
with Homebrew and adding the plugins with ``install opensearch-plugins``, or using Docker.

.. warning::

   With ``plugins.security.disabled: true``, OpenSearch accepts requests without authentication.
   OpenSearch listens only on the loopback address unless ``network.host`` is set. Before it listens
   on any other address, configure the security plugin instead; see :doc:`security`.

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

Installs the four plugins |Fess| requires into an OpenSearch you already have, in place of running
its ``bin/opensearch-plugin install`` four times. ``--opensearch-home`` is the OpenSearch
installation directory and is required. ``--version`` sets the plugin version, which must match the
OpenSearch version.

This command does not change ``opensearch.yml``. Add ``configsync.config_path`` and the other
settings yourself, as described in :doc:`install-linux` or :doc:`install-windows`.

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Downloads Node.js, which the Playwright crawler needs, into ``nodejs/`` in the |Fess| directory.
``bin/fess.in.sh`` (``bin\fess.in.bat`` on Windows) finds it there and sets
``PLAYWRIGHT_NODEJS_PATH``. With ``--dest`` outside the |Fess| directory, the command prints the
``PLAYWRIGHT_NODEJS_PATH`` line to add to ``bin/fess.in.sh`` instead. ``--version`` selects another
Node.js version. See :doc:`../config/crawler-advanced` for the Playwright crawler.

Managing Plugins
================

These commands work on the plugin directory ``app/WEB-INF/plugin`` of the |Fess| installation.
Restart |Fess| after installing, upgrading or removing plugins. Plugins can also be managed from
the System > Plugin page in the administration screen; see :doc:`../admin/plugin-guide`.

``install plugin``, ``list plugins`` and ``upgrade plugins`` accept ``--repository <url>``. It takes
the version list, the jars and their checksums from that one Maven repository, such as an internal
mirror, instead of the default release and snapshot repositories and GitHub.

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

Installs one or more |Fess| plugins, for example ``fess-script-groovy`` or ``fess-ds-git``. A name
without a version installs the newest version built for this |Fess|. ``<name>:<version>`` pins the
version of that plugin, and ``--version`` is the version for every name that has none of its own.
The previously installed version of a plugin is deleted once the new one has been installed.

A jar comes from the plugin's GitHub release, or from the Maven repository when the release has no
such asset, and is checked against the SHA-1 checksum the Maven repository publishes. A development
build of |Fess| also installs the snapshot builds of its own line, and prefers them.

See :doc:`../admin/plugin-guide` for examples.

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

Lists the plugins published for this |Fess|, and marks the installed ones with
``(installed: <version>)``. Plugins that are installed but not published in the repository, such as
a locally built jar, are listed separately. A development build of |Fess| lists the snapshot
repository as well.

list installed
--------------

::

    $ bin/fess-setup list installed

Lists the installed plugins and their versions, without contacting the repository.

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

Reinstalls every installed plugin at the version that fits this |Fess|. A plugin that is already at
that version is left as it is. The plugins in ``app/WEB-INF/plugin`` are built for one |Fess|
release, so run this command after upgrading |Fess|.

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

Deletes the installed jars of the named plugins. A name that is not installed is reported, and does
not change the exit code.

Checking an Installation
========================

list
----

::

    $ bin/fess-setup list

Shows the components that ``install`` downloads, ``opensearch`` and ``nodejs``, with the version of
each.

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

Reports on the installation, one line per check, each marked ``OK``, ``WARN`` or ``FAIL``:

- The search engine: whether it is reachable, its version (a warning when the nodes report
  different versions), whether the four plugins |Fess| requires are installed in it, and whether
  ``configsync`` responds.
- |Fess|: whether the plugin directory exists and is writable, each installed plugin (a warning for
  a plugin built for another |Fess| release, a failure for a plugin installed in two versions), and
  whether Node.js is installed in ``nodejs/`` in the |Fess| directory.

The engine URL is ``--url``, otherwise the ``SEARCH_ENGINE_HTTP_URL`` environment variable,
otherwise ``http://localhost:9200``. ``bin/fess-setup`` does not read ``bin/fess.in.sh``, so pass
``--url`` when OpenSearch is somewhere else. A missing Node.js is only reported, unless
``--playwright`` is given, which makes it a failure.

The command exits with code ``0`` when no check failed, even if some produced warnings, and with
code ``1`` otherwise.
