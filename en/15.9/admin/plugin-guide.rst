======
Plugin
======

Overview
========

The plugin settings page manages plugins.

Management Operations
=====================

Display Method
--------------

To open the installed plugin list page shown below, click [System > Plugin] in the left menu.

|image0|

To uninstall, click the Delete button.

Installation
------------

To install a new plugin, click the Install button.

|image1|

Select the plugin you want to install from the pull-down menu and click the Install button to start the installation.

Installing from the Command Line
================================

``bin/fess-setup`` installs plugins from the command line.

::

    $ bin/fess-setup install plugin fess-script-groovy

Without a version, the repository is asked for the newest one built for this |Fess|, so a different version can be installed on each run. To pin it, write the version after the plugin name, separated by a colon.

::

    $ bin/fess-setup install plugin fess-script-groovy:15.9.0 fess-ds-git:15.9.0

Plugins are released separately, so the plugins installed together are not necessarily at the same version. Give each one its own. A plugin named without a version uses the value of ``--version``.

::

    $ bin/fess-setup install plugin fess-script-groovy fess-ds-git:15.9.1 --version 15.9.0

The previously installed version of a plugin is deleted once the new one has been installed. A version that does not exist exits with code 1, so a build step such as a Dockerfile fails instead of carrying on with the plugin missing.

.. |image0| image:: ../../../resources/images/en/15.9/admin/plugin-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/plugin-2.png

