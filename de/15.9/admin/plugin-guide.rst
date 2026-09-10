=========
Plug-ins
=========

Übersicht
=========

Die Plug-in-Konfigurationsseite verwaltet Plug-ins.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite der installierten Plug-ins zu öffnen, klicken Sie im linken Menü auf [System > Plugin].

|image0|

Klicken Sie zum Deinstallieren auf die Schaltfläche „Löschen".

Installation
------------

Um ein neues Plug-in zu installieren, klicken Sie auf die Schaltfläche „Installieren".

|image1|

Wählen Sie im Dropdown-Menü das zu installierende Plug-in aus und klicken Sie auf die Schaltfläche „Installieren", um die Installation zu starten.

Installation über die Befehlszeile
==================================

``bin/fess-setup`` installiert Plug-ins über die Befehlszeile.

::

    $ bin/fess-setup install plugin fess-script-groovy

Ohne Versionsangabe wird die neueste für dieses |Fess| gebaute Version aus dem Repository gewählt, sodass bei jedem Aufruf eine andere Version installiert werden kann. Um sie festzulegen, geben Sie die Version durch einen Doppelpunkt getrennt hinter dem Plug-in-Namen an.

::

    $ bin/fess-setup install plugin fess-script-groovy:15.9.0 fess-ds-git:15.9.0

Plug-ins werden einzeln veröffentlicht, daher haben gemeinsam installierte Plug-ins nicht zwangsläufig dieselbe Version. Geben Sie die Version je Plug-in an. Für ein Plug-in ohne eigene Versionsangabe wird der Wert von ``--version`` verwendet.

::

    $ bin/fess-setup install plugin fess-script-groovy fess-ds-git:15.9.1 --version 15.9.0

Die zuvor installierte Version eines Plug-ins wird gelöscht, nachdem die neue installiert wurde. Eine nicht vorhandene Version beendet den Befehl mit dem Exit-Code 1, sodass ein Build-Schritt wie ein Dockerfile fehlschlägt, statt ohne das Plug-in fortzufahren.

.. |image0| image:: ../../../resources/images/en/15.9/admin/plugin-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/plugin-2.png
