======================
Der Befehl fess-setup
======================

``bin/fess-setup`` (unter Windows ``bin\fess-setup.bat``) liegt dem ZIP-Paket von |Fess| bei.
Es installiert, was |Fess| benötigt, aber nicht mitliefert: OpenSearch mit den von |Fess|
benötigten Plugins, Node.js für den Playwright-Crawler und |Fess|-Plugins. Außerdem prüft es eine
Installation.

Führen Sie es im |Fess|-Verzeichnis aus. Ohne Argumente gibt es die Liste der Befehle aus.

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

Exit-Codes
==========

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Bedeutung
   * - ``0``
     - Der Befehl war erfolgreich.
   * - ``1``
     - Der Befehl ist fehlgeschlagen: zum Beispiel ist ein Download fehlgeschlagen, die angeforderte
       Version existiert nicht, OpenSearch veröffentlicht für diese Plattform keinen Build, oder
       ``check`` hat ein Problem gefunden.
   * - ``2``
     - Die Befehlszeile ist fehlerhaft: ein unbekannter Befehl oder ein fehlendes Argument wie ein
       Plugin-Name.

Installation von OpenSearch und Node.js
=======================================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>]

Lädt die von diesem |Fess| unterstützte OpenSearch-Version nach ``opensearch/`` im
|Fess|-Verzeichnis herunter, installiert die vier von |Fess| benötigten Plugins
(``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash`` und
``opensearch-configsync``) und fügt der ``config/opensearch.yml`` dieser Installation die folgenden
Einstellungen hinzu:

- ``configsync.config_path``, gesetzt auf das Verzeichnis ``config/dictionary`` dieses OpenSearch
- ``plugins.security.disabled: true``

Eine Einstellung, die ``opensearch.yml`` bereits enthält, wird nicht erneut hinzugefügt, und
``plugins.security.disabled: true`` wird nicht hinzugefügt, wenn die Datei irgendeine
``plugins.security.*``-Einstellung enthält. Existiert das OpenSearch-Verzeichnis bereits, wird der
Download übersprungen; ein erneuter Aufruf für eine vorhandene Installation fügt daher nur die
fehlenden Einstellungen hinzu.

Der Befehl gibt jede hinzugefügte Einstellung aus und anschließend, ob ``bin/fess.in.sh`` dieses
OpenSearch selbst findet. Das ist der Fall, wenn es das einzige OpenSearch mit einem Verzeichnis
``config/dictionary`` unter ``opensearch/`` im |Fess|-Verzeichnis ist: ``bin/fess.in.sh`` (unter
Windows ``bin\fess.in.bat``) setzt dann ``FESS_DICTIONARY_PATH`` auf dieses Verzeichnis, und für ein
OpenSearch auf demselben Host ist nichts weiter zu konfigurieren. Andernfalls gibt der Befehl die
Werte für ``SEARCH_ENGINE_HTTP_URL`` und ``FESS_DICTIONARY_PATH`` aus, die zu setzen sind, wie in
:doc:`install-linux` oder :doc:`install-windows` beschrieben.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Beschreibung
   * - ``--dest <dir>``
     - Das Verzeichnis, in das OpenSearch entpackt wird, anstelle von ``opensearch/`` im
       |Fess|-Verzeichnis. ``bin/fess.in.sh`` sucht außerhalb dieses Verzeichnisses nicht nach
       OpenSearch.
   * - ``--version <version>``
     - Die zu installierende OpenSearch-Version. Die Plugins werden in derselben Version installiert.

OpenSearch veröffentlicht offizielle Builds nur für Linux und Windows. Auf anderen Plattformen wie
macOS beendet sich der Befehl vor jedem Download mit dem Exit-Code ``1`` und schlägt vor, OpenSearch
mit Homebrew zu installieren und die Plugins mit ``install opensearch-plugins`` hinzuzufügen oder
Docker zu verwenden.

.. warning::

   Mit ``plugins.security.disabled: true`` nimmt OpenSearch Anfragen ohne Authentifizierung an.
   OpenSearch lauscht nur auf der Loopback-Adresse, sofern ``network.host`` nicht gesetzt ist. Bevor
   es auf einer anderen Adresse lauscht, konfigurieren Sie stattdessen das Sicherheits-Plugin; siehe
   :doc:`security`.

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

Installiert die vier von |Fess| benötigten Plugins in ein bereits vorhandenes OpenSearch, anstatt
dessen ``bin/opensearch-plugin install`` viermal auszuführen. ``--opensearch-home`` ist das
Installationsverzeichnis von OpenSearch und muss angegeben werden. ``--version`` legt die
Plugin-Version fest, die mit der OpenSearch-Version übereinstimmen muss.

Dieser Befehl ändert ``opensearch.yml`` nicht. Fügen Sie ``configsync.config_path`` und die übrigen
Einstellungen selbst hinzu, wie in :doc:`install-linux` oder :doc:`install-windows` beschrieben.

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Lädt Node.js, das der Playwright-Crawler benötigt, nach ``nodejs/`` im |Fess|-Verzeichnis herunter.
``bin/fess.in.sh`` (unter Windows ``bin\fess.in.bat``) findet es dort und setzt
``PLAYWRIGHT_NODEJS_PATH``. Liegt das mit ``--dest`` angegebene Verzeichnis außerhalb des
|Fess|-Verzeichnisses, gibt der Befehl stattdessen die ``PLAYWRIGHT_NODEJS_PATH``-Zeile aus, die in
``bin/fess.in.sh`` einzutragen ist. ``--version`` wählt eine andere Node.js-Version. Zum
Playwright-Crawler siehe :doc:`../config/crawler-advanced`.

Verwaltung von Plugins
======================

Diese Befehle arbeiten mit dem Plugin-Verzeichnis ``app/WEB-INF/plugin`` der |Fess|-Installation.
Starten Sie |Fess| neu, nachdem Sie Plugins installiert, aktualisiert oder entfernt haben. Plugins
lassen sich auch über die Seite **System > Plugin** in der Administrationsoberfläche verwalten; siehe
:doc:`../admin/plugin-guide`.

``install plugin``, ``list plugins`` und ``upgrade plugins`` akzeptieren ``--repository <url>``.
Damit werden die Versionsliste, die JARs und ihre Prüfsummen aus diesem einen Maven-Repository
bezogen, etwa einem internen Mirror, statt aus den standardmäßigen Release- und
Snapshot-Repositories und von GitHub.

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

Installiert ein oder mehrere |Fess|-Plugins, zum Beispiel ``fess-script-groovy`` oder
``fess-ds-git``. Ein Name ohne Version installiert die neueste für dieses |Fess| gebaute Version.
``<name>:<version>`` legt die Version dieses Plugins fest, und ``--version`` gilt für alle Namen ohne
eigene Version. Die zuvor installierte Version eines Plugins wird gelöscht, nachdem die neue
installiert wurde.

Ein JAR wird aus dem GitHub-Release des Plugins bezogen oder aus dem Maven-Repository, wenn das
Release keine solche Datei enthält, und wird gegen die SHA-1-Prüfsumme geprüft, die das
Maven-Repository veröffentlicht. Ein Entwicklungs-Build von |Fess| installiert auch die
Snapshot-Builds seiner eigenen Versionslinie und bevorzugt diese.

Beispiele finden Sie unter :doc:`../admin/plugin-guide`.

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

Listet die für dieses |Fess| veröffentlichten Plugins auf und kennzeichnet die installierten mit
``(installed: <version>)``. Plugins, die installiert, aber nicht im Repository veröffentlicht sind,
etwa ein lokal gebautes JAR, werden gesondert aufgeführt. Ein Entwicklungs-Build von |Fess|
berücksichtigt zusätzlich das Snapshot-Repository.

list installed
--------------

::

    $ bin/fess-setup list installed

Listet die installierten Plugins und ihre Versionen auf, ohne das Repository abzufragen.

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

Installiert jedes installierte Plugin in der Version neu, die zu diesem |Fess| passt. Ein Plugin, das
bereits diese Version hat, bleibt unverändert. Die Plugins in ``app/WEB-INF/plugin`` sind für ein
bestimmtes |Fess|-Release gebaut; führen Sie diesen Befehl daher nach einem Upgrade von |Fess| aus.

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

Löscht die installierten JARs der angegebenen Plugins. Ein Name, der nicht installiert ist, wird
gemeldet und ändert den Exit-Code nicht.

Prüfen einer Installation
=========================

list
----

::

    $ bin/fess-setup list

Zeigt die Komponenten, die ``install`` herunterlädt, ``opensearch`` und ``nodejs``, jeweils mit ihrer
Version.

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

Prüft die Installation und gibt je Prüfung eine Zeile aus, gekennzeichnet mit ``OK``, ``WARN`` oder
``FAIL``:

- Die Suchmaschine: ob sie erreichbar ist, ihre Version (eine Warnung, wenn die Knoten
  unterschiedliche Versionen melden), ob die vier von |Fess| benötigten Plugins darin installiert
  sind und ob ``configsync`` antwortet.
- |Fess|: ob das Plugin-Verzeichnis existiert und beschreibbar ist, jedes installierte Plugin (eine
  Warnung für ein Plugin, das für ein anderes |Fess|-Release gebaut wurde, ein Fehler für ein
  Plugin, das in zwei Versionen installiert ist) und ob Node.js in ``nodejs/`` im
  |Fess|-Verzeichnis installiert ist.

Die URL der Suchmaschine ist ``--url``, andernfalls die Umgebungsvariable
``SEARCH_ENGINE_HTTP_URL``, andernfalls ``http://localhost:9200``. ``bin/fess-setup`` liest
``bin/fess.in.sh`` nicht; geben Sie daher ``--url`` an, wenn OpenSearch woanders läuft. Ein
fehlendes Node.js wird nur gemeldet, es sei denn, ``--playwright`` ist angegeben; dann gilt es als
Fehler.

Der Befehl endet mit dem Exit-Code ``0``, wenn keine Prüfung fehlgeschlagen ist, auch wenn einige
Prüfungen Warnungen ausgegeben haben, und andernfalls mit dem Exit-Code ``1``.
