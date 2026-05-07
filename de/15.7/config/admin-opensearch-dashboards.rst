=======================
Konfiguration der Suchprotokoll-Visualisierung
=======================

Über Suchprotokoll-Visualisierung
========================

|Fess| erfasst Suchprotokolle und Klickprotokolle von Benutzern.
Erfasste Suchprotokolle können mit `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ analysiert und visualisiert werden.

Visualisierbare Informationen
----------------

Mit Standardkonfiguration können folgende Informationen visualisiert werden:

-  Durchschnittliche Zeit für Anzeige von Suchergebnissen
-  Anzahl Suchen pro Sekunde
-  User-Agent-Ranking zugreifender Benutzer
-  Ranking der Suchschlüsselwörter
-  Ranking der Suchschlüsselwörter ohne Suchergebnisse
-  Gesamtzahl der Suchergebnisse
-  Suchtrends in Zeitreihen

Mit Visualize-Funktion können Sie neue Diagramme erstellen und zum Dashboard hinzufügen, um eigene Überwachungsdashboards zu erstellen.

Konfiguration der Datenvisualisierung mit OpenSearch Dashboards
==============================================

Installation von OpenSearch Dashboards
------------------------------------

OpenSearch Dashboards ist ein Tool zur Visualisierung von in |Fess| verwendeten OpenSearch-Daten.
Installieren Sie OpenSearch Dashboards gemäß `offizieller OpenSearch-Dokumentation <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Bearbeitung der Konfigurationsdatei
------------------

Bearbeiten Sie Konfigurationsdatei ``config/opensearch_dashboards.yml``, damit OpenSearch Dashboards in |Fess| verwendetes OpenSearch erkennt.

::

    opensearch.hosts: ["http://localhost:9201"]

Ändern Sie ``localhost`` entsprechend Ihrer Umgebung zu geeignetem Hostnamen oder IP-Adresse.
In Standardkonfiguration von |Fess| startet OpenSearch auf Port 9201.

.. note::
   Wenn OpenSearch-Portnummer abweicht, ändern Sie zu entsprechender Portnummer.

Start von OpenSearch Dashboards
-----------------------------

Nach Bearbeitung der Konfigurationsdatei starten Sie OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

Nach Start greifen Sie im Browser auf ``http://localhost:5601`` zu.

Konfiguration von Index-Mustern
--------------------------

1. Wählen Sie aus Home-Bildschirm von OpenSearch Dashboards das Menü "Management".
2. Wählen Sie "Index Patterns".
3. Klicken Sie auf "Create index pattern".
4. Geben Sie ``fess_log*`` als Index pattern name ein.
5. Klicken Sie auf "Next step".
6. Wählen Sie ``requestedAt`` als Time field.
7. Klicken Sie auf "Create index pattern".

Damit ist Vorbereitung zur Visualisierung von |Fess|-Suchprotokollen abgeschlossen.

Hauptfelder der Suchprotokolle
----------------------

|Fess|-Suchprotokolle enthalten folgende Informationen:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feldname
     - Beschreibung
   * - ``queryId``
     - Eindeutige Kennung der Suchabfrage
   * - ``searchWord``
     - Suchschlüsselwort
   * - ``requestedAt``
     - Datum und Uhrzeit der Suchausführung
   * - ``responseTime``
     - Antwortzeit der Suchergebnisse (Millisekunden)
   * - ``queryTime``
     - Abfrageausführungszeit (Millisekunden)
   * - ``hitCount``
     - Trefferanzahl der Suchergebnisse
   * - ``userAgent``
     - Browser-Informationen des Benutzers
   * - ``clientIp``
     - IP-Adresse des Clients
   * - ``languages``
     - Verwendete Sprache
   * - ``roles``
     - Rolleninformationen des Benutzers
   * - ``user``
     - Benutzername (bei Anmeldung)

Mit diesen Feldern können Sie Suchprotokolle aus verschiedenen Perspektiven analysieren.

Fehlersuche
----------------------

Wenn Daten nicht angezeigt werden
~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob OpenSearch korrekt gestartet ist.
- Überprüfen Sie, ob ``opensearch.hosts``-Einstellung in ``opensearch_dashboards.yml`` korrekt ist.
- Überprüfen Sie, ob in |Fess| Suchen ausgeführt und Protokolle aufgezeichnet werden.
- Überprüfen Sie, ob Zeitbereich des Index-Musters angemessen konfiguriert ist.

Bei Verbindungsfehlern
~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob OpenSearch-Portnummer korrekt ist.
- Überprüfen Sie Firewall- oder Sicherheitsgruppen-Einstellungen.
- Überprüfen Sie OpenSearch-Protokolldateien auf Fehler.
