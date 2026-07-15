==================================
Theme-Entwicklungsleitfaden
==================================

Übersicht
=========

Mit |Fess| können Sie das Design der Suchoberfläche auf die folgenden
zwei Arten anpassen.

Statisches Theme (Static Theme)
    Dieser Mechanismus wurde in |Fess| 15.7 eingeführt. Das Theme wird
    als ZIP-Datei verteilt, über die Administrationsoberfläche
    hochgeladen und aktiviert. Das Theme selbst ist eine eigenständige
    SPA (Single-Page-Anwendung), die die ``/api/v2/*`` API nutzt, und
    ist nicht von den JSPs des |Fess|-Kerns abhängig. Für die
    Neuentwicklung von Themes wird diese Methode empfohlen.

JAR-Theme-Plugin (Legacy)
    Dies ist der herkömmliche Plugin-Typ, der ``view`` / ``css`` /
    ``js`` / ``images`` überschreibt. Es wird als JAR gebaut und als
    Plugin installiert. Es wird verwendet, wenn Teile der bestehenden
    JSP-basierten Oberfläche ersetzt werden sollen.

.. note::

   Statische Themes stehen ab |Fess| 15.7 zur Verfügung. Wenn Sie
   Version 15.6 oder älter einsetzen, verwenden Sie ein
   JAR-Theme-Plugin. Wie Sie JSP, CSS und Bilder der Suchoberfläche
   direkt über die Administrationsoberfläche bearbeiten, erfahren Sie
   unter :doc:`../admin/design-guide`.

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
    version: "1.0.0"
    minFessVersion: "15.7"
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
     - Format nach Semantic Versioning (Beispiel: ``1.0.0``,
       ``1.2.3-beta.1``).
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
     - Die minimale |Fess|-Version, die vom Theme unterstützt wird.
   * - ``supportedLocales``
     - Optional
     - Liste der unterstützten Locales (Beispiel: ``[en, ja, de]``).
   * - ``entry``
     - Optional
     - Einstiegs-HTML der SPA. Standardwert ist ``index.html``.
   * - ``spaFallback``
     - Optional
     - Aktivierung/Deaktivierung des SPA-Fallbacks. Standardwert ist
       ``true``.

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
- Wenn ``spaFallback`` aktiviert ist, wird für die Pfade ``/``,
  ``/search``, ``/help``, ``/error``, ``/profile``, ``/cache`` und
  ``/chat`` jeweils das Einstiegs-HTML (Standard: ``index.html``)
  zurückgegeben, und das weitere Routing übernimmt die SPA.
- Die Administrationsoberfläche (``/admin/*``), ``/api/*``, die
  Anmeldeseite und Ähnliches fallen nicht unter das statische Theme und
  werden vom |Fess|-Kern selbst verarbeitet.
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

Installation und Aktivierung
------------------------------

1. Öffnen Sie in der Administrationsoberfläche „System" → „Theme"
   (``/admin/theme/``).
2. Laden Sie die erstellte ZIP-Datei hoch.
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

JAR-Theme-Plugin (Legacy)
============================

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
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

Anpassung von CSS und Bildern
--------------------------------

Die Suchoberfläche besteht aus JSPs auf Bootstrap-Basis. Sie können CSS
überschreiben, um Farbschema und Layout zu ändern, oder
``images/logo.png`` ersetzen, um das Logo zu ändern. Welche
Klassennamen und welches Markup betroffen sind, entnehmen Sie den
tatsächlichen JSPs (``view/index.jsp`` / ``view/search.jsp`` usw.).

Build und Installation
------------------------

::

    mvn clean package

Im Verzeichnis ``target/`` wird eine JAR-Datei erzeugt (Beispiel:
``fess-theme-example-15.8.0.jar``). Sie kann über die
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
- :doc:`../admin/design-guide` - Seitengestaltung (direkte Bearbeitung
  von JSP, CSS und Bildern)
- :doc:`../admin/plugin-guide` - Plugin-Installation
