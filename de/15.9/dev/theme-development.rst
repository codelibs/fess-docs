==================================
Theme-Entwicklungsleitfaden
==================================

Übersicht
=========

In |Fess| 15.9 ist die Suchoberfläche immer ein statisches Theme. Ein
statisches Theme ist eine eigenständige SPA (Single-Page-Anwendung),
die die ``/api/v2/*`` API nutzt. Themes werden als ZIP-Dateien
verteilt, über die Administrationsoberfläche hochgeladen und dort
aktiviert. Ist kein Theme ausgewählt, verwendet |Fess| ``bootstrap``,
das mitgelieferte statische Theme.

Um das Aussehen der Suchoberfläche zu ändern, installieren Sie entweder
ein anderes Theme (siehe :doc:`../admin/theme-guide`) oder erstellen ein
eigenes: Am schnellsten kopieren Sie das mitgelieferte Theme und ändern
die Kopie, wie unter `Mitgeliefertes Theme anpassen`_ beschrieben.

.. note::

   Statische Themes stehen ab |Fess| 15.7 zur Verfügung und wurden in
   15.9 zur Standard-Suchoberfläche. JAR-Theme-Plugins, die die JSPs
   der Suchoberfläche ersetzten, wurden in 15.9 entfernt; siehe
   `JAR-Theme-Plugin (in 15.9 entfernt)`_.

Statisches Theme
================

Ein statisches Theme ist eine Sammlung statischer Ressourcen, die das
``theme.yml``-Manifest und ``index.html`` enthält. Das Theme selbst
wird als Frontend-Anwendung implementiert, die die ``/api/v2/*`` API
von |Fess| aufruft.

Struktur
--------

Ein statisches Theme hat die folgende Verzeichnisstruktur.

::

    example/
    ├── theme.yml          # Manifest (erforderlich)
    ├── index.html         # Einstiegs-HTML der SPA
    ├── assets/            # Statische Ressourcen wie JavaScript und CSS
    │   └── styles.css
    ├── i18n/              # Mehrsprachige Meldungen (messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # Hilfedefinitionen (<locale>.json)
    │   └── en.json
    └── thumbnail.png      # Vorschaubild (optional)

Manifest (theme.yml)
---------------------

``theme.yml`` ist das erforderliche Manifest, das im Stammverzeichnis
des ZIP abgelegt wird. Im Folgenden sehen Sie ein Beispiel für die
minimale Konfiguration.

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "15.9.0"
    minFessVersion: "15.9"
    entry: index.html
    spaFallback: true

Die folgenden Felder können angegeben werden.

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``apiVersion``
     - Erforderlich
     - Fester Wert ``fess.codelibs.org/v1``.
   * - ``kind``
     - Erforderlich
     - Fester Wert ``StaticTheme``.
   * - ``name``
     - Erforderlich
     - Theme-Name. Muss dem Muster ``^[a-z0-9][a-z0-9_-]{0,63}$``
       entsprechen. Wird als Verzeichnisname des Themes verwendet, der
       unter ``themes/`` entpackt wird (beim Hochladen wird dieser Name
       automatisch aus ``name`` bestimmt), sowie für die
       Auslieferungs-URL (``/themes/<name>/``).
   * - ``displayName``
     - Erforderlich
     - Der in der Administrationsoberfläche angezeigte Name.
   * - ``version``
     - Erforderlich
     - Format nach Semantic Versioning (Beispiel: ``15.9.0``,
       ``15.9.1-beta.1``). Per Konvention ist ``major.minor`` die |Fess|-Linie,
       für die das Theme gebaut ist, sodass schon die Version beantwortet, für
       welches |Fess| ein Theme gedacht ist.
   * - ``author``
     - Optional
     - Name des Autors.
   * - ``description``
     - Optional
     - Beschreibung des Themes.
   * - ``license``
     - Optional
     - Lizenz.
   * - ``homepage``
     - Optional
     - URL der Homepage.
   * - ``minFessVersion``
     - Optional
     - Die minimale |Fess|-Version, die vom Theme unterstützt wird. Halten Sie sie
       gleich dem ``major.minor`` von ``version``. Ein ``maxFessVersion`` gibt es
       nicht; siehe `Veröffentlichen`_.
   * - ``supportedLocales``
     - Optional
     - Liste der unterstützten Locales (Beispiel: ``[en, ja, de]``).
   * - ``entry``
     - Optional
     - Einstiegs-HTML der SPA. Standardwert ist ``index.html``.
   * - ``spaFallback``
     - Optional
     - Veraltet. Wird aus Kompatibilitätsgründen akzeptiert, aber nicht
       mehr gelesen: Seit 15.9 wird für die Pfade der Suchoberfläche
       immer das Einstiegs-HTML ausgeliefert.

.. note::

   Beim Hochladen als ZIP wird der Name des Zielverzeichnisses
   automatisch aus ``name`` bestimmt. Wenn Sie ein Theme manuell im
   Verzeichnis ``themes/`` ablegen, muss der Verzeichnisname mit
   ``name`` übereinstimmen. Themes, deren Name nicht übereinstimmt,
   werden beim erneuten Scannen ignoriert.

.. note::

   Das Vorschau-Thumbnail wird im Stammverzeichnis des Themes unter dem
   festen Namen ``thumbnail.png`` abgelegt (es wird in der Theme-Liste
   der Administrationsoberfläche angezeigt). Dieses Bild wird anhand
   des Dateinamens erkannt, nicht über ein Feld im Manifest. Empfohlen
   wird eine Größe von maximal 512 KB und maximal 512×512 Pixeln.

Auslieferung und API
---------------------

- Statische Themes werden unter ``/themes/<name>/`` ausgeliefert
  (``<name>`` ist der Wert von ``name`` in ``theme.yml``).
- Für die Pfade ``/``, ``/search``, ``/advance``, ``/help``,
  ``/error``, ``/profile``, ``/cache`` und ``/chat`` wird jeweils das
  Einstiegs-HTML (Standard: ``index.html``) zurückgegeben, und das
  weitere Routing übernimmt die SPA. Seit 15.9 geschieht dies
  unabhängig davon, was ``spaFallback`` angibt; das Feld wird nicht
  mehr gelesen.
- Auch Fehler werden vom Theme dargestellt: Schlägt eine Anfrage fehl,
  erhält ein Browser das Einstiegs-HTML des Themes unter der
  angeforderten URL, mit dem tatsächlichen HTTP-Status.
- Die Administrationsoberfläche (``/admin/*``), ``/api/*``, die
  Anmeldeseite und Ähnliches fallen nicht unter das statische Theme und
  werden vom |Fess|-Kern selbst verarbeitet.
- ``{{themePath}}`` im Einstiegs-HTML wird bei der Auslieferung durch
  ``themes/<name>`` ersetzt. Verweisen Sie in ``index.html`` auf die
  eigenen Dateien des Themes als ``{{themePath}}/assets/styles.css`` usw.
  Der Theme-Name steht dann nicht in der Seite, sodass das Theme unter
  jedem Namen, unter dem es installiert ist, seine eigenen Dateien lädt.
- Das Einstiegs-HTML wird mit einem ``Content-Security-Policy``-Header
  ausgeliefert, der Skripte, Stylesheets, Bilder und Verbindungen nur
  von |Fess| selbst zulässt (Inline-Styles sind erlaubt, Inline-Skripte
  nicht). Schriften oder Skripte von einem externen CDN werden daher
  nicht geladen; liefern Sie sie im Theme mit.
- Die SPA des Themes ruft Daten wie Suchergebnisse und Chat über die
  ``/api/v2/*`` API ab.

Packaging
---------

Mit ``scripts/package.sh`` aus dem Repository
`fess-themes <https://github.com/codelibs/fess-themes>`__ können Sie
das Theme zu einem ZIP für die Verteilung zusammenfassen.

::

    ./scripts/package.sh example

Es wird ``dist/example-<version>.zip`` erzeugt (``<version>`` ist der
Wert von ``version`` in ``theme.yml``).

.. note::

   ``theme.yml`` muss im Stammverzeichnis des ZIP abgelegt werden. Wird
   die Datei in einem Unterverzeichnis abgelegt, wird sie beim
   Hochladen nicht erkannt.

Veröffentlichen
---------------

Die vom |Fess|-Projekt entwickelten Themes werden unter
https://maven.codelibs.org/release/org/codelibs/fess/themes/ veröffentlicht, als
``<name>/<version>/<name>-<version>.zip`` mit einer ``.sha1`` daneben und einer
``maven-metadata.xml`` je Theme, die die veröffentlichten Versionen auflistet.
``bin/fess-setup install theme <name>`` liest diese Metadaten, um die Version zu wählen, die für
das laufende |Fess| gebaut wurde.

Versionieren Sie ein Theme auf der |Fess|-Linie, für die es gedacht ist, und erhöhen Sie die
Version immer dann, wenn sich ändert, was das Archiv ausliefert. Eine veröffentlichte Version wird
nie überschrieben, eine Änderung unter derselben Version wird also schlicht nie verteilt.

Aus demselben Grund gibt es im Manifest kein Feld für eine Obergrenze. Weil ein veröffentlichtes
Archiv sich nie ändert, ließe sich eine Obergrenze später nicht ergänzen, wenn ein Theme auf einem
neueren |Fess| nicht mehr läuft. Das Theme für die neuere Linie nicht zu veröffentlichen sagt
dasselbe -- zu dem Zeitpunkt, an dem man es weiß.

.. note::

   Ermitteln Sie die veröffentlichten Versionen aus ``maven-metadata.xml`` statt aus einer
   Verzeichnisauflistung. Der Verzeichnisindex wird periodisch erzeugt, ein frisch
   veröffentlichtes Theme ist also über seine Metadaten lesbar, bevor es in einer Auflistung
   auftaucht.

Installation und Aktivierung
------------------------------

1. Öffnen Sie in der Administrationsoberfläche „System" → „Theme"
   (``/admin/theme/``).
2. Laden Sie die erstellte ZIP-Datei hoch. Ein veröffentlichtes Theme lässt sich
   stattdessen mit ``bin/fess-setup install theme <name>`` von der Kommandozeile
   installieren; siehe :doc:`../install/fess-setup`.
3. Wählen Sie auf der Listenseite im Dropdown-Menü „Standard-Theme" das
   gewünschte Theme aus, und klicken Sie auf die Schaltfläche
   „Festlegen", um es zu aktivieren.

Der Aktivierungsmechanismus funktioniert wie folgt.

- Beim Klicken auf die Schaltfläche „Festlegen" wird der Name des
  ausgewählten Themes in der Systemeigenschaft ``theme.default``
  gespeichert und wird so zum systemweiten Standard-Theme.
- Wenn der Theme-Name mit dem Schlüssel eines virtuellen Hosts
  übereinstimmt, wird das Theme nur beim Zugriff auf diesen virtuellen
  Host angewendet. Dadurch kann das Theme pro virtuellem Host
  umgeschaltet werden.
- Wenn Sie das Verzeichnis ``themes/`` direkt auf der Festplatte
  aktualisieren, können Sie mit „Neu laden" ein erneutes Scannen
  auslösen.

.. note::

   Für das Hochladen von ZIP-Dateien gelten Obergrenzen für
   Dateigröße, Gesamtgröße nach dem Entpacken und Anzahl der Einträge;
   diese lassen sich über die ``theme.*``-Eigenschaften in
   ``fess_config.properties`` anpassen (Beispiel:
   ``theme.upload.max.size`` beträgt standardmäßig 50MB,
   ``theme.directory.path`` ist standardmäßig ``themes``). Beim
   Entpacken werden Prüfungen durchgeführt, um Angriffe durch ZIP Slip
   und Zip Bombs zu verhindern.

.. _theme-customize-bundled:

Mitgeliefertes Theme anpassen
-----------------------------

Das mitgelieferte Theme ``bootstrap`` liegt in ``app/themes/bootstrap/``
der |Fess|-Installation (``/usr/share/fess/app/themes/bootstrap/`` bei
den RPM/DEB-Paketen). Bearbeiten Sie es nicht direkt: Ein Upgrade
ersetzt es, und der Name ``bootstrap`` ist dafür reserviert, sodass es
weder gelöscht noch durch einen Upload ersetzt werden kann. Kopieren
Sie es stattdessen unter einem neuen Namen.

1. Kopieren Sie das Verzeichnis, zum Beispiel nach ``mytheme``::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. Ändern Sie in ``theme.yml`` den Wert ``name`` in ``mytheme`` und
   ändern Sie ``displayName``. ``name`` muss mit dem Verzeichnisnamen
   übereinstimmen.

3. Lassen Sie ``index.html`` unverändert. Die mitgelieferte
   ``index.html`` verweist auf ihre eigenen Dateien, etwa das Stylesheet,
   die Logos und das Skript, als ``{{themePath}}/assets/...``, und |Fess|
   ersetzt ``{{themePath}}`` bei der Auslieferung durch ``themes/<name>``
   (den ``name`` in ``theme.yml``). Das Umbenennen genügt daher, damit die
   Kopie ihre eigenen Dateien lädt. Wenn Sie eine Datei hinzufügen, auf die
   ``index.html`` verweist, schreiben Sie ihre URL ebenfalls als
   ``{{themePath}}/assets/...``.

4. Nehmen Sie Ihre Änderungen vor:

   - Farben und Layout: ``assets/styles.css``.
   - Logos: ``assets/logo-head.png`` (Kopfzeile) und ``assets/logo.png``
     (Startseite der Suche).
   - Texte, etwa die Fußzeile (``footer.copyright_org``): die Dateien
     ``i18n/messages.<locale>.json``, eine pro Sprache.
   - Seitenstruktur: ``index.html``.

5. Packen Sie das Verzeichnis als ZIP mit ``theme.yml`` im
   Stammverzeichnis und laden Sie es in der Administrationsoberfläche
   unter „System" → „Theme" hoch::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   Alternativ legen Sie das Verzeichnis in ``app/themes/`` ab und
   klicken auf derselben Seite auf „Neu laden".

6. Wählen Sie auf dieser Seite ``mytheme`` als Standard-Theme aus.

.. note::

   Ersetzen Sie die Kopie nach jedem |Fess|-Upgrade durch eine neue
   Kopie des mitgelieferten Themes und wenden Sie Ihre Änderungen
   erneut an, da das mitgelieferte Theme der ``/api/v2/*`` API seiner
   |Fess|-Version folgt.

JAR-Theme-Plugin (in 15.9 entfernt)
====================================

Der Typ JAR-Theme-Plugin, der JSPs, CSS und Bilder in einem ``fess-theme-*``-JAR bündelte
und sie als das nach dem Schlüssel eines virtuellen Hosts benannte Theme anwendete, wurde in
|Fess| 15.9 entfernt. 15.9 entpackt kein JAR-Theme und verwendet es für keinen Bildschirm.

- Wenn Sie eines über „System" → „Plugin" in der Verwaltungsoberfläche installieren, wird es
  nur als allgemeines JAR vom Typ ``jar`` in ``app/WEB-INF/plugin/`` abgelegt; kein
  Bildschirm ändert sich. Ein aus einer früheren Version verbliebenes ``fess-theme-*.jar``
  wird ebenso aufgeführt und kann auf dieser Seite oder mit
  ``bin/fess-setup remove plugin <name>`` gelöscht werden.
- ``bin/fess-setup`` listet ``fess-theme-*`` weder auf noch installiert es sie.

Übertragen Sie die Änderungen aus einem JAR-Theme in ein statisches Theme:

- Für Farben, Layout und Logo der Suchoberfläche kopieren Sie das mitgelieferte Theme und
  ändern die Kopie (siehe `Mitgeliefertes Theme anpassen`_).
- Wenn Sie das Aussehen pro virtuellem Host geändert haben, installieren Sie ein statisches
  Theme, das nach dem virtuellen Host benannt ist (siehe :doc:`../config/security-virtual-host`).
- Der Anmeldebildschirm (``/login/``) ist für alle virtuellen Hosts derselbe. Ein Theme
  kann ihn nicht ändern.

Beispiele für vorhandene Themes
===================================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - Sammlung
  statischer Themes (enthält mehrere statische Themes wie
  ``codesearch`` und ``docsearch``)

Referenzinformationen
=========================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../admin/plugin-guide` - Plugin-Installation
