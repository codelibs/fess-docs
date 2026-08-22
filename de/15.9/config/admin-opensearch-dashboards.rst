==============================================
Konfiguration der Suchprotokoll-Visualisierung
==============================================

Über die Suchprotokoll-Visualisierung
======================================

|Fess| erfasst Suchprotokolle und Klickprotokolle von Benutzern.
Die erfassten Suchprotokolle können mit `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ analysiert und visualisiert werden.

|Fess| enthält die Dashboard-Definitionsdatei ``extension/kibana/fess_log.ndjson`` zur Visualisierung von Suchprotokollen.
Durch den Import dieser Datei in OpenSearch Dashboards können die vorbereiteten Dashboards sofort verwendet werden.

Visualisierbare Informationen
-----------------------------

Wenn die mitgelieferte Dashboard-Definition (``fess_log.ndjson``) importiert wird, werden das ``fess_log``-Dashboard und die folgenden sechs Visualisierungen registriert.

-  Durchschnittliche Antwortzeit für die Anzeige von Suchergebnissen (``average-response-time``)
-  Anzahl der Suchanfragen pro Zeiteinheit (``search-query-counts-per-sec``)
-  User-Agent-Ranking der zugreifenden Benutzer (``rank-of-UserAgent``)
-  Ranking der Suchschlüsselwörter (``search-term-rank``)
-  Ranking der Suchschlüsselwörter ohne Suchergebnisse (``search-term-rank-of-no-results``)
-  Durchschnittliche Trefferanzahl der Suchergebnisse (``hit-counts``)

Zusätzlich dazu können mit der Visualize-Funktion neue Diagramme erstellt und zum Dashboard hinzugefügt werden, um ein eigenes Überwachungs-Dashboard aufzubauen.

Konfiguration der Datenvisualisierung mit OpenSearch Dashboards
===============================================================

Installation von OpenSearch Dashboards
---------------------------------------

OpenSearch Dashboards ist ein Tool zur Visualisierung von OpenSearch-Daten, die in |Fess| verwendet werden.
Installieren Sie OpenSearch Dashboards gemäß der `offiziellen OpenSearch-Dokumentation <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Bearbeitung der Konfigurationsdatei
-------------------------------------

Bearbeiten Sie die Konfigurationsdatei ``config/opensearch_dashboards.yml``, damit OpenSearch Dashboards das in |Fess| verwendete OpenSearch erkennt.

::

    opensearch.hosts: ["http://localhost:9201"]

Ändern Sie ``localhost`` entsprechend Ihrer Umgebung zu einem geeigneten Hostnamen oder einer IP-Adresse.
In der Standardkonfiguration von |Fess| startet OpenSearch auf Port 9201.

.. note::
   Wenn die Portnummer von OpenSearch abweicht, ändern Sie sie auf die entsprechende Portnummer.

Start von OpenSearch Dashboards
---------------------------------

Nach der Bearbeitung der Konfigurationsdatei starten Sie OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

Nach dem Start greifen Sie im Browser auf ``http://localhost:5601`` zu.

Konfiguration von Index-Mustern
----------------------------------

Erstellen Sie ein Index-Muster zur Visualisierung von Suchprotokollen.

1. Wählen Sie im linken Menü „Management" (bei manchen Versionen von OpenSearch Dashboards „Dashboards Management").
2. Wählen Sie „Index Patterns".
3. Klicken Sie auf „Create index pattern".
4. Geben Sie ``fess_log*`` als Index pattern name ein.
5. Klicken Sie auf „Next step".
6. Wählen Sie ``requestedAt`` als Time field.
7. Klicken Sie auf „Create index pattern".

.. note::
   Die Suchprotokolle von |Fess| werden in mehreren Indizes gespeichert, die mit ``fess_log`` beginnen, z. B. ``fess_log.search_log`` für Suchprotokolle und ``fess_log.click_log`` für Klickprotokolle.
   Durch die Angabe des Index-Musters ``fess_log*`` können alle diese Indizes zusammen abgedeckt werden.

Import der Dashboard-Definition
----------------------------------

Durch den Import der mitgelieferten Dashboard-Definition von |Fess| können die vorbereiteten Visualisierungen und Dashboards verwendet werden.

1. Wählen Sie im linken Menü „Management" (bei manchen Versionen von OpenSearch Dashboards „Dashboards Management").
2. Wählen Sie „Saved Objects".
3. Klicken Sie auf „Import".
4. Wählen Sie ``extension/kibana/fess_log.ndjson`` im Installationsverzeichnis von |Fess|.
5. Klicken Sie auf „Import", um den Import auszuführen.

Nach Abschluss des Imports werden sechs Visualisierungen und das ``fess_log``-Dashboard registriert.

Dashboard-Anzeige
-------------------

1. Wählen Sie im linken Menü „Dashboard".
2. Wählen Sie das ``fess_log``-Dashboard.
3. Die Visualisierungsergebnisse der Suchprotokolle werden angezeigt.
4. Mit der Zeitbereichsauswahl oben rechts können Sie den anzuzeigenden Zeitraum festlegen.

Erstellen eigener Visualisierungen
------------------------------------

Zusätzlich zum mitgelieferten Dashboard können auch eigene Visualisierungen und Dashboards erstellt werden.

Erstellen einer Visualisierung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Wählen Sie im linken Menü „Visualize".
2. Klicken Sie auf „Create visualization".
3. Wählen Sie den Visualisierungstyp (Liniendiagramm, Kreisdiagramm, Balkendiagramm usw.).
4. Wählen Sie das erstellte Index-Muster ``fess_log*``.
5. Konfigurieren Sie die erforderlichen Metriken und Buckets (Aggregationseinheiten).
6. Klicken Sie auf „Save", um die Visualisierung zu speichern.

Erstellen eines Dashboards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Wählen Sie im linken Menü „Dashboard".
2. Klicken Sie auf „Create dashboard".
3. Klicken Sie auf „Add", um die erstellten Visualisierungen hinzuzufügen.
4. Passen Sie das Layout an und klicken Sie auf „Save", um zu speichern.

Zeitzoneneinstellung
----------------------

Wenn die Zeitanzeige nicht korrekt ist, konfigurieren Sie die Zeitzone.

1. Wählen Sie im linken Menü „Management" (bei manchen Versionen von OpenSearch Dashboards „Dashboards Management").
2. Wählen Sie „Advanced Settings".
3. Suchen Sie nach ``dateFormat:tz``.
4. Legen Sie die Zeitzone auf einen geeigneten Wert fest (z. B. ``Asia/Tokyo`` oder ``UTC``).
5. Klicken Sie auf „Save".

Überprüfung der Protokolldaten
--------------------------------

1. Wählen Sie im linken Menü „Discover".
2. Wählen Sie das Index-Muster ``fess_log*``.
3. Die Daten der Suchprotokolle werden angezeigt.
4. Mit der Zeitbereichsauswahl oben rechts können Sie den anzuzeigenden Zeitraum festlegen.

Hauptfelder der Suchprotokolle
--------------------------------

Die Suchprotokolle von |Fess| (``fess_log.search_log``) enthalten folgende Informationen:

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
     - Gesamte Antwortzeit des Suchvorgangs (Millisekunden)
   * - ``queryTime``
     - Ausführungszeit der Abfrage an die Suchmaschine (Millisekunden)
   * - ``hitCount``
     - Trefferanzahl der Suchergebnisse
   * - ``hitCountRelation``
     - Gibt an, ob die Trefferanzahl ein exakter Wert oder ein Mindestwert ist (``eq``: exakte Anzahl, ``gte``: mindestens dieser Wert)
   * - ``queryOffset``
     - Startposition für den Abruf der Suchergebnisse
   * - ``queryPageSize``
     - Anzahl der angezeigten Einträge pro Seite
   * - ``userAgent``
     - Browser-Informationen des Benutzers
   * - ``referer``
     - Referenz-URL der Seite, von der die Suche ausgeführt wurde
   * - ``clientIp``
     - IP-Adresse des Clients
   * - ``languages``
     - Verwendete Sprache der Anfrage
   * - ``accessType``
     - Zugriffstyp (``web``, ``json``, ``gsa``, ``admin``, ``other``)
   * - ``roles``
     - Rolleninformationen des Benutzers
   * - ``user``
     - Benutzername (bei Anmeldung)
   * - ``virtualHost``
     - Virtueller Hostname (wenn konfiguriert)

Mit diesen Feldern können Suchprotokolle aus verschiedenen Perspektiven analysiert werden.

Fehlersuche
-------------

Wenn Daten nicht angezeigt werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob OpenSearch korrekt gestartet ist.
- Überprüfen Sie, ob die ``opensearch.hosts``-Einstellung in ``opensearch_dashboards.yml`` korrekt ist.
- Überprüfen Sie, ob in |Fess| Suchen ausgeführt und Protokolle aufgezeichnet werden.
- Überprüfen Sie, ob der Zeitbereich oben rechts den Zeitraum einschließt, in dem Protokolle aufgezeichnet wurden.
- Wenn die Zeitanzeige abweicht, überprüfen Sie die Einstellung von ``dateFormat:tz``.

Bei Verbindungsfehlern
~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Portnummer von OpenSearch korrekt ist.
- Überprüfen Sie die Firewall- oder Sicherheitsgruppen-Einstellungen.
- Überprüfen Sie die OpenSearch-Protokolldateien auf Fehler.
