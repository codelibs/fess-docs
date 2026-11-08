======================================================================
Teil 22: Eine Wissenslandkarte der Organisation aus Suchdaten zeichnen
======================================================================

Einleitung
==========

Ein Suchsystem ist ein Werkzeug zum "Finden" von Informationen, doch die Suchprotokolle selbst sind ebenfalls eine wertvolle Informationsquelle.
"Was wird gesucht?", "Was kann nicht gefunden werden?", "Welche Informationen werden häufig aufgerufen?" -- diese Daten dienen als Spiegel, der die Informationsbedürfnisse und Wissenslücken der Organisation widerspiegelt.

In diesem Artikel kombinieren wir die Suchprotokolle von Fess mit OpenSearch Dashboards, um ein Analyse-Dashboard zu erstellen, das die Wissensnutzung der Organisation visualisiert.

Zielgruppe
==========

- Personen, die die Nutzung ihres Suchsystems quantitativ erfassen möchten
- Personen, die Daten für Strategien zur Informationsnutzung sammeln möchten
- Personen, die die grundlegende Bedienung von OpenSearch Dashboards kennenlernen möchten

Der Wert von Suchdaten
======================

Was Suchprotokolle verraten
----------------------------

Suchprotokolle sind eine seltene Art von Daten, die es ermöglichen, die Informationsbedürfnisse einer Organisation quantitativ zu erfassen.

.. list-table:: Erkenntnisse aus Suchdaten
   :header-rows: 1
   :widths: 30 70

   * - Daten
     - Erkenntnis
   * - Suchbegriffe
     - Wonach Mitarbeiter suchen (Informationsbedürfnisse)
   * - Nulltreffer-Abfragen
     - In der Organisation fehlende Informationen (Wissenslücken)
   * - Klickprotokolle
     - Welche Suchergebnisse nützlich waren (Inhaltswert)
   * - Suchhäufigkeit im Zeitverlauf
     - Veränderungen der Informationsbedürfnisse (Trends)
   * - Beliebte Wörter
     - Themen von Interesse in der gesamten Organisation

Von Fess erfasste Daten
=========================

Fess erfasst und speichert automatisch die folgenden Daten.

Suchprotokolle (``fess_log.search_log``)
------------------------------------------

Diese können in der Administrationsoberfläche unter [Systeminformationen] > [Suchprotokoll] eingesehen werden.
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
     - Ausführungszeit der Abfrage (Millisekunden)
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
     - Abfrage-ID (wird zur Verknüpfung mit Klickprotokollen verwendet)

Klickprotokolle (``fess_log.click_log``)
-----------------------------------------

Dies sind Aufzeichnungen darüber, wann Links in Suchergebnissen angeklickt wurden.
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
     - queryId aus dem Suchprotokoll (identifiziert, welche Suche zum Klick führte)
   * - ``order``
     - integer
     - Anzeigeposition in den Suchergebnissen
   * - ``requestedAt``
     - date
     - Datum und Uhrzeit des Klicks
   * - ``docId``
     - keyword
     - Dokument-ID

Beliebte Wörter
------------------

Die auf der Suchoberfläche angezeigten beliebten Wörter werden aus Suchprotokollen im Suggest-Index von Fess aggregiert.
Abfragen, die eine bestimmte Anzahl von Suchtreffern überschreiten, werden basierend auf der Suchhäufigkeit eingestuft.

Visualisierung mit OpenSearch Dashboards
==========================================

Da die Suchprotokolle von Fess in OpenSearch gespeichert werden, ist eine erweiterte Visualisierung mit OpenSearch Dashboards möglich.

Einrichtung von OpenSearch Dashboards
---------------------------------------

Fügen Sie OpenSearch Dashboards zu Ihrer Docker-Compose-Konfiguration hinzu.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: public.ecr.aws/opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Greifen Sie auf ``http://localhost:5601`` zu, um die Dashboards-Oberfläche zu verwenden.

Erstellen von Indexmustern
----------------------------

Um Fess-Protokolldaten in OpenSearch Dashboards zu visualisieren, müssen Sie zunächst Indexmuster erstellen.

1. Greifen Sie auf Dashboards zu und wählen Sie im linken Menü [Stack Management] > [Index Patterns]
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
Erstellen Sie jede Visualisierung über [Visualize] im linken Menü und fassen Sie sie in einem [Dashboard] zusammen.

Übersicht der Suchnutzung
----------------------------

**Tägliche Suchanfragen im Zeitverlauf**

Verstehen Sie, wie sich die Suchnutzung im Laufe der Zeit verändert.

- Indexmuster: ``fess_log.search_log``
- Visualisierung: Line (Liniendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1d)
- Y-Achse: Count

Wenn die Nutzung zunimmt, ist dies ein Beleg dafür, dass sich das Suchsystem etabliert hat; wenn sie abnimmt, sind Verbesserungen erforderlich.

**Suchanfragen nach Tageszeit**

Verstehen Sie, zu welchen Tageszeiten die meisten Suchanfragen gestellt werden.

- Visualisierung: Vertical Bar (Balkendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1h)
- Y-Achse: Count

Wenn zu Arbeitsbeginn oder nach der Mittagspause vermehrt gesucht wird, zeigt dies, dass die Informationsbeschaffung zu einem festen Bestandteil der täglichen Arbeit geworden ist.

Analyse der Suchqualität
---------------------------

**Entwicklung der Nulltrefferrate**

Die Nulltrefferrate ist ein wichtiger Indikator für die Suchqualität.
Datensätze, bei denen das Feld ``hitCount`` im Suchprotokoll den Wert ``0`` hat, entsprechen Nulltreffer-Abfragen.

- Indexmuster: ``fess_log.search_log``
- Filter: ``hitCount: 0`` hinzufügen, um Nulltreffer-Abfragen zu extrahieren
- Visualisierung: Line (Liniendiagramm)
- X-Achse: Date Histogram (Feld: ``requestedAt``, Intervall: 1d)
- Y-Achse: Count

Wenn die Nulltrefferrate hoch ist, müssen Synonyme hinzugefügt oder der Crawling-Bereich erweitert werden (siehe Teil 8).

Beachten Sie, dass Sie eine Liste der Nulltreffer-Abfragen auch in der Administrationsoberfläche unter [Systeminformationen] > [Suchprotokoll] einsehen können.

**Wortwolke der Nulltreffer-Abfragen**

Die Darstellung von Nulltreffer-Abfragen als Wortwolke bietet einen schnellen Überblick darüber, welche Informationen fehlen.

- Filter: ``hitCount: 0``
- Visualisierung: Tag Cloud
- Feld: Terms Aggregation (Feld: ``searchWord``, Größe: 50)

Analyse des Inhaltswerts
--------------------------

**Am häufigsten angeklickte Suchergebnisse**

Häufig angeklickte Suchergebnisse stellen wertvolle Inhalte für die Organisation dar.

- Indexmuster: ``fess_log.click_log``
- Visualisierung: Data Table
- Feld: Terms Aggregation (Feld: ``url``, Größe: 20, Sortierung: Count absteigend)

Priorisieren Sie die Pflege und Aktualisierung dieser Inhalte.

**Verteilung der Klickpositionen**

Überprüfen Sie die Verteilung, an welcher Position in den Suchergebnissen geklickt wird.

- Indexmuster: ``fess_log.click_log``
- Visualisierung: Vertical Bar (Balkendiagramm)
- X-Achse: Histogram (Feld: ``order``, Intervall: 1)
- Y-Achse: Count

Wenn die Positionen 1-3 die meisten Klicks erhalten, ist die Suchqualität gut; wenn Position 10 und höher viele Klicks erhalten, sind Ranking-Verbesserungen erforderlich.

Trendanalyse der Informationsbedürfnisse
-------------------------------------------

**Ranking beliebter Suchbegriffe**

Verstehen Sie, wofür sich die Organisation insgesamt interessiert.

- Indexmuster: ``fess_log.search_log``
- Visualisierung: Data Table
- Feld: Terms Aggregation (Feld: ``searchWord``, Größe: 20, Sortierung: Count absteigend)

Veränderungen bei den beliebten Suchbegriffen spiegeln Veränderungen der Herausforderungen und Interessen der Organisation wider.

Nutzung der Analyseergebnisse
===============================

Die Ergebnisse der Suchdatenanalyse können für die folgenden Maßnahmen genutzt werden.

Content-Strategie
------------------

- **Nulltreffer-Abfragen**: Fehlende Inhalte identifizieren und deren Erstellung beauftragen
- **Beliebte Suchbegriffe**: Informationen zu häufig gesuchten Themen erweitern
- **Ergebnisse mit niedriger Klickrate**: Verbesserung oder Entfernung von Inhalten in Betracht ziehen

Verbesserung der Suchqualität
--------------------------------

- **Synonyme hinzufügen**: Synonymkandidaten aus Nulltreffer-Abfragen ermitteln
- **Key-Match-Konfiguration**: Optimale Ergebnisse für beliebte Abfragen festlegen
- **Boost-Anpassung**: Rankings basierend auf Klickraten verbessern

IT-Investitionsentscheidungen
-------------------------------

- **Steigende Nutzung**: Planung zur Erweiterung der Serverressourcen
- **Neue Informationsbedürfnisse**: Anbindung zusätzlicher Datenquellen in Betracht ziehen
- **Bedarf an KI-Funktionen**: Entscheidung über die Einführung des KI-Suchmodus (siehe Teil 19)

Erstellen regelmäßiger Berichte
===================================

Fassen Sie Analyseergebnisse in regelmäßigen Berichten zusammen und teilen Sie diese mit den Beteiligten.

Beispiel für monatliche Berichtspunkte
------------------------------------------

1. Zusammenfassung der Suchnutzung (Gesamtanzahl der Suchanfragen, Vergleich zum Vormonat)
2. Entwicklung der Nulltrefferrate und Verbesserungsstatus
3. Top 10 der beliebten Suchbegriffe
4. Neu entdeckte Wissenslücken
5. Durchgeführte Verbesserungsmaßnahmen und deren Auswirkungen
6. Verbesserungspläne für den nächsten Monat

Zusammenfassung
================

In diesem Artikel haben wir erläutert, wie Sie mithilfe von Suchprotokollen die Wissensnutzung in Ihrer Organisation visualisieren können.

- Erkenntnisse aus Suchprotokollen (Informationsbedürfnisse, Wissenslücken, Inhaltswert)
- Aufbau von Visualisierungs-Dashboards mit OpenSearch Dashboards
- Anwendung der Analyseergebnisse auf Content-Strategie, Verbesserung der Suchqualität und IT-Investitionen
- Kontinuierliche Verbesserung durch regelmäßige Berichte

Suchdaten sind ein wertvolles Gut, um eine "Wissenslandkarte der Organisation" zu zeichnen.
Damit schließt der Abschnitt zu KI und Suche der nächsten Generation ab. In der nächsten und letzten Folge werden wir eine Gesamtzusammenfassung der Serie präsentieren.

Referenzen
==========

- `Fess Suchprotokoll <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
