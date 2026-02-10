==================================
Laststeuerung-Konfiguration
==================================

Uebersicht
==========

|Fess| enthaelt eine Laststeuerungsfunktion, die Anfragen basierend auf der CPU-Auslastung von OpenSearch steuert.
Diese Funktion begrenzt Anfragen bei hoher Suchmaschinenlast automatisch und schuetzt die Systemstabilitaet.

Funktionen der Laststeuerung:

- Echtzeitueberwachung der OpenSearch-Cluster-CPU-Auslastung
- Unabhaengige Schwellenwerte fuer Web-Anfragen und API-Anfragen
- Gibt HTTP 429 (Too Many Requests) zurueck, wenn Schwellenwerte ueberschritten werden
- Admin-Panel, Login und statische Ressourcen sind von der Steuerung ausgenommen
- Standardmaessig deaktiviert (Schwellenwert=100)

Konfiguration
=============

Setzen Sie die folgenden Eigenschaften in ``fess_config.properties``:

::

    # CPU-Auslastungs-Schwellenwert fuer Web-Anfragen (%)
    # Anfragen werden abgelehnt, wenn die CPU-Auslastung diesen Wert erreicht oder ueberschreitet
    # Auf 100 setzen zum Deaktivieren (Standard: 100)
    web.load.control=100

    # CPU-Auslastungs-Schwellenwert fuer API-Anfragen (%)
    # Anfragen werden abgelehnt, wenn die CPU-Auslastung diesen Wert erreicht oder ueberschreitet
    # Auf 100 setzen zum Deaktivieren (Standard: 100)
    api.load.control=100

    # CPU-Auslastungs-Ueberwachungsintervall (Sekunden)
    # Intervall zum Abrufen der OpenSearch-Cluster-CPU-Auslastung
    # Standard: 1
    load.control.monitor.interval=1

.. note::
   Wenn sowohl ``web.load.control`` als auch ``api.load.control`` auf 100 (Standard) gesetzt sind,
   ist die Laststeuerungsfunktion vollstaendig deaktiviert und die Ueberwachung wird nicht gestartet.

Funktionsweise
==============

Ueberwachungsmechanismus
------------------------

Wenn die Laststeuerung aktiviert ist (ein Schwellenwert unter 100), ueberwacht LoadControlMonitorTarget regelmaessig die CPU-Auslastung des OpenSearch-Clusters.

- Ruft OS-Statistiken von allen Knoten im OpenSearch-Cluster ab
- Zeichnet die hoechste CPU-Auslastung aller Knoten auf
- Ueberwacht im durch ``load.control.monitor.interval`` angegebenen Intervall (Standard: 1 Sekunde)
- Die Ueberwachung wird verzoegert beim ersten Request gestartet

.. note::
   Wenn das Abrufen der Ueberwachungsinformationen fehlschlaegt, wird die CPU-Auslastung auf 0 zurueckgesetzt.
   Nach 3 aufeinanderfolgenden Fehlern aendert sich das Loglevel von WARNING zu DEBUG.

Anfragesteuerung
----------------

Wenn eine Anfrage eintrifft, verarbeitet LoadControlFilter sie in folgender Reihenfolge:

1. Pruefen, ob der Pfad ausgenommen ist (wenn ausgenommen, durchlassen)
2. Art der Anfrage bestimmen (Web / API)
3. Entsprechenden Schwellenwert abrufen
4. Wenn der Schwellenwert 100 oder hoeher ist, nicht steuern (durchlassen)
5. Aktuelle CPU-Auslastung mit dem Schwellenwert vergleichen
6. Wenn CPU-Auslastung >= Schwellenwert, HTTP 429 zurueckgeben

**Ausgenommene Anfragen:**

- Pfade, die mit ``/admin`` beginnen (Admin-Panel)
- Pfade, die mit ``/error`` beginnen (Fehlerseiten)
- Pfade, die mit ``/login`` beginnen (Login-Seiten)
- Statische Ressourcen (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Fuer Web-Anfragen:**

- Gibt HTTP 429-Statuscode zurueck
- Zeigt die Fehlerseite (``busy.jsp``) an

**Fuer API-Anfragen:**

- Gibt HTTP 429-Statuscode zurueck
- Gibt eine JSON-Antwort zurueck:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

Konfigurationsbeispiele
=======================

Nur Web-Anfragen begrenzen
---------------------------

Konfiguration, die nur Web-Suchanfragen begrenzt und API nicht einschraenkt:

::

    # Web: Anfragen bei CPU-Auslastung von 80% oder mehr ablehnen
    web.load.control=80

    # API: Keine Einschraenkung
    api.load.control=100

    # Ueberwachungsintervall: 1 Sekunde
    load.control.monitor.interval=1

Web und API begrenzen
---------------------

Beispiel mit unterschiedlichen Schwellenwerten fuer Web und API:

::

    # Web: Anfragen bei CPU-Auslastung von 70% oder mehr ablehnen
    web.load.control=70

    # API: Anfragen bei CPU-Auslastung von 80% oder mehr ablehnen
    api.load.control=80

    # Ueberwachungsintervall: 2 Sekunden
    load.control.monitor.interval=2

.. note::
   Wenn Sie den API-Schwellenwert hoeher als den Web-Schwellenwert setzen, koennen Sie eine gestufte Steuerung erreichen,
   bei der zuerst Web-Anfragen bei hoher Last eingeschraenkt werden und API-Anfragen erst bei weiter steigender Last
   ebenfalls eingeschraenkt werden.

Unterschied zur Rate-Limitierung
================================

|Fess| verfuegt ueber eine :doc:`rate-limiting`-Funktion, die von der Laststeuerung getrennt ist.
Diese schuetzen das System mit unterschiedlichen Ansaetzen.

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
     - Verhinderung uebermaeessiger Anfragen
     - Schutz der Suchmaschine vor hoher Last
   * - Begrenzungseinheit
     - Pro IP-Adresse
     - Systemweit
   * - Antwort
     - HTTP 429
     - HTTP 429
   * - Anwendungsbereich
     - Such-API / AI-Modus-API
     - Web-Anfragen / API-Anfragen

Die Kombination beider Funktionen ermoeglicht einen robusteren Systemschutz.

Fehlerbehebung
==============

Laststeuerung wird nicht aktiviert
----------------------------------

**Ursache**: Konfiguration wird nicht richtig angewendet

**Pruefen**:

1. Ist ``web.load.control`` oder ``api.load.control`` unter 100 gesetzt?
2. Wird die Konfigurationsdatei korrekt gelesen?
3. Wurde |Fess| neu gestartet?

Legitime Anfragen werden abgelehnt
-----------------------------------

**Ursache**: Schwellenwerte sind zu niedrig

**Loesungen**:

1. Die Werte von ``web.load.control`` oder ``api.load.control`` erhoehen
2. ``load.control.monitor.interval`` anpassen, um die Ueberwachungshaeufigkeit zu aendern
3. Ressourcen des OpenSearch-Clusters erweitern

.. warning::
   Wenn Schwellenwerte zu niedrig gesetzt werden, koennen Anfragen auch bei normaler Last abgelehnt werden.
   Ueberpruefen Sie die normale CPU-Auslastung Ihres OpenSearch-Clusters, bevor Sie geeignete Schwellenwerte festlegen.

Referenzinformationen
=====================

- :doc:`rate-limiting` - Rate-Limiting-Konfiguration
