============================================================
Teil 22: Eine Wissenslandkarte der Organisation aus Suchdaten zeichnen -- Informationsnutzung im Analyse-Dashboard verstehen
============================================================

Einleitung
==========

Ein Suchsystem ist ein Werkzeug zum "Finden" von Informationen, doch die Suchprotokolle selbst sind ebenfalls eine wertvolle Informationsquelle.
"Was wird gesucht?", "Was kann nicht gefunden werden?", "Welche Informationen werden haeufig aufgerufen?" -- diese Daten dienen als Spiegel, der die Informationsbeduerfnisse und Wissensluecken der Organisation widerspiegelt.

In diesem Artikel kombinieren wir die Suchprotokolle von Fess mit OpenSearch Dashboards, um ein Analyse-Dashboard zu erstellen, das die Wissensnutzung der Organisation visualisiert.

Zielgruppe
==========

- Personen, die die Nutzung ihres Suchsystems quantitativ erfassen moechten
- Personen, die Daten fuer Strategien zur Informationsnutzung sammeln moechten
- Personen, die die grundlegende Bedienung von OpenSearch Dashboards kennenlernen moechten

Der Wert von Suchdaten
======================

Was Suchprotokolle verraten
----------------------------

Suchprotokolle sind eine seltene Art von Daten, die es ermoeglichen, die Informationsbeduerfnisse einer Organisation quantitativ zu erfassen.

.. list-table:: Erkenntnisse aus Suchdaten
   :header-rows: 1
   :widths: 30 70

   * - Daten
     - Erkenntnis
   * - Suchbegriffe
     - Wonach Mitarbeiter suchen (Informationsbeduerfnisse)
   * - Nulltreffer-Abfragen
     - In der Organisation fehlende Informationen (Wissensluecken)
   * - Klickprotokolle
     - Welche Suchergebnisse nuetzlich waren (Inhaltswert)
   * - Suchhaeufigkeit im Zeitverlauf
     - Veraenderungen der Informationsbeduerfnisse (Trends)
   * - Beliebte Woerter
     - Themen von Interesse in der gesamten Organisation

Von Fess erfasste Daten
=========================

Fess erfasst und speichert automatisch die folgenden Daten.

Suchprotokolle (``fess_log.search_log``)
------------------------------------------

Diese koennen in der Administrationsoberflaeche unter [Systeminformationen] > [Suchprotokoll] eingesehen werden.
Sie werden im OpenSearch-Index ``fess_log.search_log`` gespeichert.

Wichtige Felder:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feldname
     - Typ
     - Beschreibung
   * - ``searchWord``
     - keyword
     - Suchbegriff
   * - ``requestedAt``
     - date
     - Datum und Uhrzeit der Suche
   * - ``hitCount``
     - long
     - Anzahl der Suchergebnisse (0 bedeutet Nulltreffer)
   * - ``queryTime``
     - long
     - Ausfuehrungszeit der Abfrage (Millisekunden)
   * - ``responseTime``
     - long
     - Gesamte Antwortzeit (Millisekunden)
   * - ``userAgent``
     - keyword
     - User-Agent
   * - ``clientIp``
     - keyword
     - Client-IP-Adresse
   * - ``accessType``
     - keyword
     - Zugriffstyp (web, json, gsa, admin usw.)
   * - ``queryId``
     - keyword
     - Abfrage-ID (wird zur Verknuepfung mit Klickprotokollen verwendet)

Klickprotokolle (``fess_log.click_log``)
-----------------------------------------

Dies sind Aufzeichnungen darueber, wann Links in Suchergebnissen angeklickt wurden.
Sie werden im OpenSearch-Index ``fess_log.click_log`` gespeichert.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feldname
     - Typ
     - Beschreibung
   * - ``url``
     - keyword
     - Angeklickte URL
   * - ``queryId``
     - keyword
     - queryId aus dem Suchprotokoll (identifiziert, welche Suche zum Klick fuehrte)
   * - ``order``
     - integer
     - Anzeigeposition in den Suchergebnissen
   * - ``requestedAt``
     - date
     - Datum und Uhrzeit des Klicks
   * - ``docId``
     - keyword
     - Dokument-ID

Beliebte Woerter
------------------

Die auf der Suchoberflaeche angezeigten beliebten Woerter werden aus Suchprotokollen im Suggest-Index von Fess aggregiert.
Abfragen, die eine bestimmte Anzahl von Suchtreffern ueberschreiten, werden basierend auf der Suchhaeufigkeit eingestuft.

Visualisierung mit OpenSearch Dashboards
==========================================

Da die Suchprotokolle von Fess in OpenSearch gespeichert werden, ist eine erweiterte Visualisierung mit OpenSearch Dashboards moeglich.

Einrichtung von OpenSearch Dashboards
---------------------------------------

Fuegen Sie OpenSearch Dashboards zu Ihrer Docker-Compose-Konfiguration hinzu.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Greifen Sie auf ``http://localhost:5601`` zu, um die Dashboards-Oberflaeche zu verwenden.

Erstellen von Indexmustern
----------------------------

Um Fess-Protokolldaten in OpenSearch Dashboards zu visualisieren, muessen Sie zunaechst Indexmuster erstellen.

1. Greifen Sie auf Dashboards zu und waehlen Sie im linken Menue [Stack Management] > [Index Patterns]
2. Klicken Sie auf [Create index pattern]
3. Erstellen Sie die folgenden Indexmuster

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Indexmuster
     - Zeitfeld
     - Verwendungszweck
   * - ``fess_log.search_log``
     - ``requestedAt``
     - Analyse der Suchprotokolle
   * - ``fess_log.click_log``
     - ``requestedAt``
     - Analyse der Klickprotokolle

Dashboard-Design
==================

Entwerfen Sie das Dashboard mit den folgenden Analyseperspektiven.
Erstellen Sie jede Visualisierung ueber [Visualize] im linken Menue und fassen Sie sie in einem [Dashboard] zusammen.

Uebersicht der Suchnutzung
----------------------------

**Taegliche Suchanfragen im Zeitverlauf**

Verstehen Sie, wie sich die Suchnutzung im Laufe der Zeit veraendert.

- Indexmuster: ``fess_log.search_log``
- Visualisierung: Line (Liniendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1d)
- Y-Achse: Count

Wenn die Nutzung zunimmt, ist dies ein Beleg dafuer, dass sich das Suchsystem etabliert hat; wenn sie abnimmt, sind Verbesserungen erforderlich.

**Suchanfragen nach Tageszeit**

Verstehen Sie, zu welchen Tageszeiten die meisten Suchanfragen gestellt werden.

- Visualisierung: Vertical Bar (Balkendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1h)
- Y-Achse: Count

Wenn zu Arbeitsbeginn oder nach der Mittagspause vermehrt gesucht wird, zeigt dies, dass die Informationsbeschaffung zu einem festen Bestandteil der taeglichen Arbeit geworden ist.

Analyse der Suchqualitaet
---------------------------

**Entwicklung der Nulltrefferrate**

Die Nulltrefferrate ist ein wichtiger Indikator fuer die Suchqualitaet.
Datensaetze, bei denen das Feld ``hitCount`` im Suchprotokoll den Wert ``0`` hat, entsprechen Nulltreffer-Abfragen.

- Indexmuster: ``fess_log.search_log``
- Filter: ``hitCount: 0`` hinzufuegen, um Nulltreffer-Abfragen zu extrahieren
- Visualisierung: Line (Liniendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1d)
- Y-Achse: Count

Wenn die Nulltrefferrate hoch ist, muessen Synonyme hinzugefuegt oder der Crawling-Bereich erweitert werden (siehe Teil 8).

Beachten Sie, dass Sie eine Liste der Nulltreffer-Abfragen auch in der Administrationsoberflaeche unter [Systeminformationen] > [Suchprotokoll] einsehen koennen.

**Wortwolke der Nulltreffer-Abfragen**

Die Darstellung von Nulltreffer-Abfragen als Wortwolke bietet einen schnellen Ueberblick darueber, welche Informationen fehlen.

- Filter: ``hitCount: 0``
- Visualisierung: Tag Cloud
- Feld: Terms Aggregation (Feld: ``searchWord``, Groesse: 50)

Analyse des Inhaltswerts
--------------------------

**Am haeufigsten angeklickte Suchergebnisse**

Haeufig angeklickte Suchergebnisse stellen wertvolle Inhalte fuer die Organisation dar.

- Indexmuster: ``fess_log.click_log``
- Visualisierung: Data Table
- Feld: Terms Aggregation (Feld: ``url``, Groesse: 20, Sortierung: Count absteigend)

Priorisieren Sie die Pflege und Aktualisierung dieser Inhalte.

**Verteilung der Klickpositionen**

Ueberpruefen Sie die Verteilung, an welcher Position in den Suchergebnissen geklickt wird.

- Indexmuster: ``fess_log.click_log``
- Visualisierung: Vertical Bar (Balkendiagramm)
- X-Achse: Histogram (Feld: ``order``, Intervall: 1)
- Y-Achse: Count

Wenn die Positionen 1-3 die meisten Klicks erhalten, ist die Suchqualitaet gut; wenn Position 10 und hoeher viele Klicks erhalten, sind Ranking-Verbesserungen erforderlich.

Trendanalyse der Informationsbeduerfnisse
-------------------------------------------

**Ranking beliebter Suchbegriffe**

Verstehen Sie, wofuer sich die Organisation insgesamt interessiert.

- Indexmuster: ``fess_log.search_log``
- Visualisierung: Data Table
- Feld: Terms Aggregation (Feld: ``searchWord``, Groesse: 20, Sortierung: Count absteigend)

Veraenderungen bei den beliebten Suchbegriffen spiegeln Veraenderungen der Herausforderungen und Interessen der Organisation wider.

Nutzung der Analyseergebnisse
===============================

Die Ergebnisse der Suchdatenanalyse koennen fuer die folgenden Massnahmen genutzt werden.

Content-Strategie
------------------

- **Nulltreffer-Abfragen**: Fehlende Inhalte identifizieren und deren Erstellung beauftragen
- **Beliebte Suchbegriffe**: Informationen zu haeufig gesuchten Themen erweitern
- **Ergebnisse mit niedriger Klickrate**: Verbesserung oder Entfernung von Inhalten in Betracht ziehen

Verbesserung der Suchqualitaet
--------------------------------

- **Synonyme hinzufuegen**: Synonymkandidaten aus Nulltreffer-Abfragen ermitteln
- **Key-Match-Konfiguration**: Optimale Ergebnisse fuer beliebte Abfragen festlegen
- **Boost-Anpassung**: Rankings basierend auf Klickraten verbessern

IT-Investitionsentscheidungen
-------------------------------

- **Steigende Nutzung**: Planung zur Erweiterung der Serverressourcen
- **Neue Informationsbeduerfnisse**: Anbindung zusaetzlicher Datenquellen in Betracht ziehen
- **Bedarf an KI-Funktionen**: Entscheidung ueber die Einfuehrung des KI-Suchmodus (siehe Teil 19)

Erstellen regelmaessiger Berichte
===================================

Fassen Sie Analyseergebnisse in regelmaessigen Berichten zusammen und teilen Sie diese mit den Beteiligten.

Beispiel fuer monatliche Berichtspunkte
------------------------------------------

1. Zusammenfassung der Suchnutzung (Gesamtanzahl der Suchanfragen, Vergleich zum Vormonat)
2. Entwicklung der Nulltrefferrate und Verbesserungsstatus
3. Top 10 der beliebten Suchbegriffe
4. Neu entdeckte Wissensluecken
5. Durchgefuehrte Verbesserungsmassnahmen und deren Auswirkungen
6. Verbesserungsplaene fuer den naechsten Monat

Zusammenfassung
================

In diesem Artikel haben wir erlaeutert, wie Sie mithilfe von Suchprotokollen die Wissensnutzung in Ihrer Organisation visualisieren koennen.

- Erkenntnisse aus Suchprotokollen (Informationsbeduerfnisse, Wissensluecken, Inhaltswert)
- Aufbau von Visualisierungs-Dashboards mit OpenSearch Dashboards
- Anwendung der Analyseergebnisse auf Content-Strategie, Verbesserung der Suchqualitaet und IT-Investitionen
- Kontinuierliche Verbesserung durch regelmaessige Berichte

Suchdaten sind ein wertvolles Gut, um eine "Wissenslandkarte der Organisation" zu zeichnen.
Damit schliesst der Abschnitt zu KI und Suche der naechsten Generation ab. In der naechsten und letzten Folge werden wir eine Gesamtzusammenfassung der Serie praesentieren.

Referenzen
==========

- `Fess Suchprotokoll <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
