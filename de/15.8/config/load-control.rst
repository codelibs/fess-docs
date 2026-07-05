============================
Laststeuerung-Konfiguration
============================

Übersicht
=========

|Fess| enthält zwei Arten von Laststeuerungsfunktionen, die die Systemstabilität basierend auf der CPU-Auslastung schützen.

**HTTP-Anfragen-Laststeuerung** (``web.load.control`` / ``api.load.control``):

- Echtzeitüberwachung der CPU-Auslastung des OpenSearch-Clusters
- Unabhängige Schwellenwerte für Web-Anfragen und API-Anfragen konfigurierbar
- Gibt HTTP 429 (Too Many Requests) zurück, wenn Schwellenwerte überschritten werden
- Admin-Panel, Login und statische Ressourcen sind von der Steuerung ausgenommen
- Standardmäßig deaktiviert (Schwellenwert=100)

**Adaptive Laststeuerung** (``adaptive.load.control``):

- Überwacht die System-CPU-Auslastung des Fess-Servers selbst
- Drosselt automatisch Hintergrundaufgaben wie Crawling, Indexierung, Suggest-Aktualisierungen und Thumbnail-Generierung
- Wenn die CPU-Auslastung den Schwellenwert erreicht oder überschreitet, werden Verarbeitungsthreads angehalten und bei Unterschreitung fortgesetzt
- Standardmäßig aktiviert (Schwellenwert=50)

Konfiguration der HTTP-Anfragen-Laststeuerung
=============================================

Setzen Sie die folgenden Eigenschaften in ``fess_config.properties``:

::

    # CPU-Auslastungs-Schwellenwert für Web-Anfragen (%)
    # Anfragen werden abgelehnt, wenn die OpenSearch-CPU-Auslastung diesen Wert erreicht oder überschreitet
    # Auf 100 setzen zum Deaktivieren (Standard: 100)
    web.load.control=100

    # CPU-Auslastungs-Schwellenwert für API-Anfragen (%)
    # Anfragen werden abgelehnt, wenn die OpenSearch-CPU-Auslastung diesen Wert erreicht oder überschreitet
    # Auf 100 setzen zum Deaktivieren (Standard: 100)
    api.load.control=100

    # Überwachungsintervall der CPU-Auslastung (Sekunden)
    # Intervall zum Abrufen der CPU-Auslastung des OpenSearch-Clusters
    # Standard: 1
    load.control.monitor.interval=1

.. note::
   Wenn sowohl ``web.load.control`` als auch ``api.load.control`` auf 100 (Standard) gesetzt sind,
   wird die OpenSearch-CPU-Überwachung nicht gestartet.

Funktionsweise
==============

Überwachungsmechanismus
-----------------------

Wenn die Laststeuerung aktiviert ist (ein Schwellenwert unter 100), überwacht LoadControlMonitorTarget regelmäßig die CPU-Auslastung des OpenSearch-Clusters.

- Ruft OS-Statistiken von allen Knoten im OpenSearch-Cluster ab
- Zeichnet die höchste CPU-Auslastung aller Knoten auf
- Überwacht im durch ``load.control.monitor.interval`` angegebenen Intervall (Standard: 1 Sekunde)
- Die Überwachung wird verzögert initialisiert und beim ersten Request gestartet

.. note::
   Wenn das Abrufen der Überwachungsinformationen fehlschlägt, wird die CPU-Auslastung auf 0 zurückgesetzt.
   Bei den ersten drei aufeinanderfolgenden Fehlern wird dies auf WARNING-Ebene protokolliert, ab dem vierten Fehler wird auf DEBUG-Ebene gewechselt
   (um eine übermäßige Protokollvergrößerung durch anhaltende Fehler zu verhindern). Sobald die Überwachung einmal erfolgreich ist, wird der Fehlerzähler zurückgesetzt.

Anfragesteuerung
----------------

Wenn eine Anfrage eintrifft, verarbeitet LoadControlFilter sie in folgender Reihenfolge:

1. Prüfen, ob der Pfad ausgenommen ist (wenn ausgenommen, durchlassen)
2. Art der Anfrage bestimmen (Web / API)
3. Entsprechenden Schwellenwert abrufen
4. Wenn der Schwellenwert 100 oder höher ist, nicht steuern (durchlassen)
5. Aktuelle CPU-Auslastung mit dem Schwellenwert vergleichen
6. Wenn CPU-Auslastung >= Schwellenwert, HTTP 429 zurückgeben

**Ausgenommene Anfragen:**

- Pfade, die mit ``/admin`` beginnen (Admin-Panel)
- Pfade, die mit ``/error`` beginnen (Fehlerseiten)
- Pfade, die mit ``/login`` beginnen (Login-Seiten)
- Statische Ressourcen (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Für Web-Anfragen:**

- Gibt HTTP 429-Statuscode zurück
- Zeigt die Fehlerseite (``busy.jsp``) an

**Für API-Anfragen:**

- Gibt HTTP 429-Statuscode zurück
- Fügt den HTTP-Antwort-Header ``Retry-After: 60`` hinzu
- Gibt eine JSON-Antwort zurück:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

.. note::
   Wenn eine Anfrage abgelehnt wird, wird auf INFO-Ebene im Server-Log
   ``Rejecting request due to high CPU load: path=..., cpu=...%, threshold=...%``
   ausgegeben. Damit lässt sich nachvollziehen, welcher Pfad mit welchem Schwellenwert abgelehnt wurde.

Konfigurationsbeispiele
=======================

Nur Web-Anfragen begrenzen
--------------------------

Konfiguration, die nur Web-Suchanfragen begrenzt und API nicht einschränkt:

::

    # Web: Anfragen bei CPU-Auslastung von 80 % oder mehr ablehnen
    web.load.control=80

    # API: Keine Einschränkung
    api.load.control=100

    # Überwachungsintervall: 1 Sekunde
    load.control.monitor.interval=1

Web und API begrenzen
---------------------

Beispiel mit unterschiedlichen Schwellenwerten für Web und API:

::

    # Web: Anfragen bei CPU-Auslastung von 70 % oder mehr ablehnen
    web.load.control=70

    # API: Anfragen bei CPU-Auslastung von 80 % oder mehr ablehnen
    api.load.control=80

    # Überwachungsintervall: 2 Sekunden
    load.control.monitor.interval=2

.. note::
   Wenn Sie den API-Schwellenwert höher als den Web-Schwellenwert setzen, können Sie eine gestufte Steuerung erreichen,
   bei der zuerst Web-Anfragen bei hoher Last eingeschränkt werden und API-Anfragen erst bei weiter steigender Last
   ebenfalls eingeschränkt werden.

Unterschied zur Rate-Limitierung
=================================

|Fess| verfügt über eine :doc:`rate-limiting`-Funktion, die von der Laststeuerung getrennt ist.
Diese schützen das System mit unterschiedlichen Ansätzen.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspekt
     - Rate-Limitierung
     - Laststeuerung
   * - Steuerungsgrundlage
     - Anzahl der Anfragen (pro Zeiteinheit)
     - OpenSearch CPU-Auslastung
   * - Zweck
     - Verhinderung übermäßiger Anfragen
     - Schutz der Suchmaschine vor hoher Last
   * - Begrenzungseinheit
     - Pro IP-Adresse
     - Systemweit
   * - Antwort
     - HTTP 429
     - HTTP 429
   * - Anwendungsbereich
     - Alle HTTP-Anfragen
     - Web-Anfragen / API-Anfragen (Admin-Panel usw. ausgenommen)

Die Kombination beider Funktionen ermöglicht einen robusteren Systemschutz.

Adaptive Laststeuerung
======================

Die adaptive Laststeuerung passt die Verarbeitungsgeschwindigkeit von Hintergrundaufgaben
automatisch basierend auf der System-CPU-Auslastung des Fess-Servers an.

Konfiguration
-------------

``fess_config.properties``:

::

    # CPU-Auslastungs-Schwellenwert für die adaptive Laststeuerung (%)
    # Hält Hintergrundaufgaben an, wenn die System-CPU-Auslastung diesen Wert erreicht oder überschreitet
    # Auf 0 oder darunter setzen zum Deaktivieren (Standard: 50)
    adaptive.load.control=50

Verhalten
---------

- Überwacht die System-CPU-Auslastung des Servers, auf dem Fess läuft
- Wenn die CPU-Auslastung den Schwellenwert erreicht oder überschreitet, warten die betroffenen Verarbeitungsthreads, bis die CPU-Auslastung unter den Schwellenwert fällt
- Wenn die CPU-Auslastung unter den Schwellenwert fällt, wird die Verarbeitung automatisch fortgesetzt

**Betroffene Hintergrundaufgaben:**

- Crawling (Web / Dateisystem)
- Indexierung (Dokumentenregistrierung)
- Datenspeicher-Verarbeitung
- Suggest-Aktualisierungen
- Thumbnail-Generierung
- Sicherung und Wiederherstellung

.. note::
   Die adaptive Laststeuerung ist standardmäßig aktiviert (Schwellenwert=50).
   Sie arbeitet unabhängig von der HTTP-Anfragen-Laststeuerung (``web.load.control`` / ``api.load.control``).

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspekt
     - HTTP-Anfragen-Laststeuerung
     - Adaptive Laststeuerung
   * - Überwachungsziel
     - OpenSearch CPU-Auslastung
     - System-CPU-Auslastung des Fess-Servers
   * - Steuerungsziel
     - HTTP-Anfragen (Web / API)
     - Hintergrundaufgaben
   * - Steuerungsmethode
     - Lehnt Anfragen mit HTTP 429 ab
     - Hält Verarbeitungsthreads vorübergehend an
   * - Standard
     - Deaktiviert (Schwellenwert=100)
     - Aktiviert (Schwellenwert=50)

Fehlerbehebung
==============

Laststeuerung wird nicht aktiviert
-----------------------------------

**Ursache**: Konfiguration wird nicht richtig angewendet

**Prüfen**:

1. Ist ``web.load.control`` oder ``api.load.control`` unter 100 gesetzt?
2. Wird die Konfigurationsdatei korrekt gelesen?
3. Wurde |Fess| neu gestartet?

Legitime Anfragen werden abgelehnt
------------------------------------

**Ursache**: Schwellenwerte sind zu niedrig

**Lösungen**:

1. Die Werte von ``web.load.control`` oder ``api.load.control`` erhöhen
2. ``load.control.monitor.interval`` anpassen, um die Überwachungshäufigkeit zu ändern
3. Ressourcen des OpenSearch-Clusters erweitern

.. warning::
   Wenn Schwellenwerte zu niedrig gesetzt werden, können Anfragen auch bei normaler Last abgelehnt werden.
   Überprüfen Sie die normale CPU-Auslastung Ihres OpenSearch-Clusters, bevor Sie geeignete Schwellenwerte festlegen.

Crawling ist langsam
--------------------

**Ursache**: Threads befinden sich aufgrund der adaptiven Laststeuerung im Wartezustand

**Prüfen**:

1. Ob ``Cpu Load XX% is greater than YY%`` in den Logs erscheint
2. Ob der ``adaptive.load.control``-Schwellenwert zu niedrig ist

**Lösungen**:

1. Den Wert von ``adaptive.load.control`` erhöhen (z. B. 70)
2. CPU-Ressourcen des Fess-Servers erweitern
3. Auf 0 setzen, um die adaptive Laststeuerung zu deaktivieren (nicht empfohlen)

Referenzinformationen
=====================

- :doc:`rate-limiting` - Rate-Limiting-Konfiguration
