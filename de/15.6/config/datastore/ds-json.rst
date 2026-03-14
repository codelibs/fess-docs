==================================
JSON-Konnektor
==================================

Übersicht
=========

Der JSON-Konnektor bietet die Funktionalität, Daten aus JSON-Dateien oder JSON-APIs abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-json`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Zugriff auf die JSON-Datei oder API ist erforderlich
3. Die JSON-Struktur muss bekannt sein

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Platzieren
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Über die Administrationsoberfläche installieren

1. Öffnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
3. Starten Sie |Fess| neu

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Products JSON
   * - Handler-Name
     - JsonDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Lokale Datei:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

HTTP-Datei:

::

    files=https://api.example.com/products.json
    fileEncoding=UTF-8

REST-API (mit Authentifizierung):

::

    files=https://api.example.com/v1/items
    fileEncoding=UTF-8

Mehrere Dateien:

::

    files=/path/to/data1.json,https://api.example.com/data2.json
    fileEncoding=UTF-8

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``files``
     - Ja
     - Pfad zur JSON-Datei oder API-URL (mehrere kommagetrennt)
   * - ``fileEncoding``
     - Nein
     - Zeichenkodierung (Standard: UTF-8)
