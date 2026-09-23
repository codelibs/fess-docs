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
   der Suchoberfläche ersetzen, ändern die Suchoberfläche in 15.9 nicht
   mehr; siehe `JAR-Theme-Plugin (Legacy)`_.

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

3. Ersetzen Sie in ``index.html`` jedes ``themes/bootstrap/`` durch
   ``themes/mytheme/``. Die mitgelieferte ``index.html`` nennt ihr
   eigenes Verzeichnis an vier Stellen: das Stylesheet
   (``assets/styles.css``), die beiden Logos (``assets/logo-head.png``
   und ``assets/logo.png``) und das Skript (``assets/app.js``). Bleiben
   sie unverändert, lädt die Kopie weiterhin die Dateien von
   ``bootstrap``, und keine Ihrer Änderungen an CSS, Logos oder
   Meldungen wird sichtbar. Die übrigen Dateien werden relativ zu
   ``assets/app.js`` geladen, daher sind nur diese vier zu ändern.

   ::

       $ sed -i 's#themes/bootstrap/#themes/mytheme/#g' /tmp/mytheme/index.html

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

JAR-Theme-Plugin (Legacy)
============================

.. warning::

   Seit |Fess| 15.9 wird die Suchoberfläche immer von einem statischen
   Theme ausgeliefert, daher ändert ein JAR-Theme-Plugin sie nicht mehr.
   Von den JSPs, die ein JAR-Theme bereitstellt, werden nur noch die der
   Anmeldeseite (``/login/``) verwendet. Übertragen Sie das Design in ein
   statisches Theme; siehe `Mitgeliefertes Theme anpassen`_.

Ein JAR-Theme-Plugin ist ein Plugin, das die Verzeichnisse ``view`` /
``css`` / ``js`` / ``images`` des |Fess|-Kerns pro Theme-Name
überschreibt. Zur allgemeinen Struktur und Build-Methode von Plugins
siehe auch :doc:`plugin-architecture`.

Struktur
--------

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # JSP-Dateien (search.jsp, index.jsp, header.jsp usw.)
        ├── css/       # CSS-Dateien (style.css usw.)
        ├── js/        # JavaScript-Dateien
        └── images/    # Bilddateien (logo.png usw.)

.. note::

   Views (Templates) liegen im JSP-Format vor. Als oberste
   Ressourcenverzeichnisse werden nur die vier Verzeichnisse ``view`` /
   ``css`` / ``js`` / ``images`` erkannt. Der Artefaktname muss mit
   ``fess-theme-`` beginnen.

pom.xml
-------

Das Plugin wird als jar mit ``fess-parent`` als übergeordnetem POM
gebaut. Da ein Theme ausschließlich aus Ressourcen besteht, müssen in
der Regel keine zusätzlichen Abhängigkeiten deklariert werden.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

Anpassung von CSS und Bildern
--------------------------------

Die JSPs basieren auf Bootstrap. Sie können CSS überschreiben, um
Farbschema und Layout zu ändern, oder ``images/logo.png`` ersetzen, um
das Logo zu ändern. Seit 15.9 wirkt sich dies nur auf die Anmeldeseite
aus; die Suchoberfläche ist ein statisches Theme (siehe
`Mitgeliefertes Theme anpassen`_).

Build und Installation
------------------------

::

    mvn clean package

Im Verzeichnis ``target/`` wird eine JAR-Datei erzeugt (Beispiel:
``fess-theme-example-15.9.0.jar``). Sie kann über die
Administrationsoberfläche unter „System" → „Plugin" installiert
werden. Details zum Installationsvorgang finden Sie unter
:doc:`../admin/plugin-guide`.

Nach der Installation werden die einzelnen Verzeichnisse im JAR pro
Theme-Name an folgende Orte entpackt (der Theme-Name ist der Teil des
Artefaktnamens ohne das Präfix ``fess-theme-``; im obigen Beispiel
``example``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Verzeichnis im JAR
     - Zielort
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

Aktivierung
-----------

JAR-Themes werden über die Funktion für virtuelle Hosts aktiviert.
Wenn Sie den Schlüssel eines virtuellen Hosts mit dem Theme-Namen
abgleichen, wird das Theme beim Zugriff auf diesen Host angewendet.

1. Ordnen Sie in den Einstellungen für virtuelle Hosts unter „System"
   → „Allgemein" den ``Host``-Header der Anfrage dem Theme-Namen
   (Schlüssel des virtuellen Hosts) zu, zum Beispiel
   ``Host:localhost:8080=example``.
2. Legen Sie bei Bedarf denselben Namen (``example``) auch für
   virtuelle Hosts an anderen Stellen fest, etwa in den
   Web-Crawling-Einstellungen.

Details zur Konfiguration virtueller Hosts finden Sie unter
:doc:`../admin/general-guide`.

Beispiele für vorhandene Themes
===================================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - Sammlung
  statischer Themes (enthält mehrere statische Themes wie
  ``codesearch`` und ``docsearch``)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
  - JAR-Theme
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__
  - JAR-Theme

Referenzinformationen
=========================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../admin/plugin-guide` - Plugin-Installation
