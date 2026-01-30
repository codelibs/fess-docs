==================================
Skripting-Uebersicht
==================================

Uebersicht
==========

|Fess| ermoeglicht es Ihnen, in verschiedenen Szenarien benutzerdefinierte Logik mithilfe von Skripten zu implementieren.
Durch die Nutzung von Skripten koennen Sie die Datenverarbeitung waehrend des Crawlings,
die Anpassung von Suchergebnissen und die Ausfuehrung geplanter Aufgaben flexibel steuern.

Unterstuetzte Skriptsprachen
============================

|Fess| unterstuetzt die folgenden Skriptsprachen:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Sprache
     - Bezeichner
     - Beschreibung
   * - Groovy
     - ``groovy``
     - Die Standard-Skriptsprache. Java-kompatibel mit leistungsstarken Funktionen
   * - JavaScript
     - ``javascript``
     - Eine fuer Webentwickler vertraute Sprache

.. note::
   Groovy wird am haeufigsten verwendet, und die Beispiele in dieser Dokumentation sind in Groovy geschrieben.

Anwendungsfaelle fuer Skripte
=============================

Datenspeicher-Konfiguration
---------------------------

Datenspeicher-Konnektoren verwenden Skripte, um abgerufene Daten auf Indexfelder abzubilden.

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

Pfad-Mapping
------------

Skripte koennen fuer URL-Normalisierung und Pfadkonvertierung verwendet werden.

::

    # URL transformieren
    url.replaceAll("http://", "https://")

Geplante Aufgaben
-----------------

Geplante Aufgaben ermoeglichen es Ihnen, benutzerdefinierte Verarbeitungslogik in Groovy-Skripten zu schreiben.

::

    return container.getComponent("crawlJob").execute();

Grundlegende Syntax
===================

Variablenzugriff
----------------

::

    # Auf Datenspeicherdaten zugreifen
    data.fieldName

    # Auf Systemkomponenten zugreifen
    container.getComponent("componentName")

Zeichenkettenoperationen
------------------------

::

    # Verkettung
    title + " - " + category

    # Ersetzung
    content.replaceAll("old", "new")

    # Aufteilung
    tags.split(",")

Bedingte Verzweigung
--------------------

::

    # Ternaerer Operator
    data.status == "active" ? "Aktiv" : "Inaktiv"

    # Null-Pruefung
    data.description ?: "Keine Beschreibung"

Datumsoperationen
-----------------

::

    # Aktuelles Datum/Uhrzeit
    new Date()

    # Formatierung
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

Verfuegbare Objekte
===================

Hauptobjekte, die innerhalb von Skripten verfuegbar sind:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Objekt
     - Beschreibung
   * - ``data``
     - Aus dem Datenspeicher abgerufene Daten
   * - ``container``
     - DI-Container (Zugriff auf Komponenten)
   * - ``systemHelper``
     - System-Helfer
   * - ``fessConfig``
     - |Fess| Konfiguration

Sicherheit
==========

.. warning::
   Skripte haben leistungsstarke Faehigkeiten, verwenden Sie sie daher nur aus vertrauenswuerdigen Quellen.

- Skripte werden auf dem Server ausgefuehrt
- Zugriff auf das Dateisystem und Netzwerk ist moeglich
- Stellen Sie sicher, dass nur Benutzer mit Administratorrechten Skripte bearbeiten koennen

Leistung
========

Tipps zur Optimierung der Skriptleistung:

1. **Komplexe Verarbeitung vermeiden**: Skripte werden fuer jedes Dokument ausgefuehrt
2. **Zugriff auf externe Ressourcen minimieren**: Netzwerkaufrufe verursachen Verzoegerungen
3. **Caching verwenden**: Erwaegen Sie das Caching von Werten, die wiederholt verwendet werden

Debugging
=========

Verwenden Sie Protokollausgaben zum Debuggen von Skripten:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

Protokollebenen-Konfiguration:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

Referenzinformationen
=====================

- :doc:`scripting-groovy` - Groovy-Skripting-Leitfaden
- :doc:`../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- :doc:`../admin/scheduler-guide` - Scheduler-Konfigurationsleitfaden
