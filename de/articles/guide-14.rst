===============================================
Teil 14: Skalierungsstrategien für Suchsysteme
===============================================

Einführung
============

Wenn Sie Fess zunachst in kleinem Umfang einführen, entstehen mit wachsender Nutzung unweigerlich Anforderungen wie "mehr Dokumente", "mehr Benutzer" und "schnellere Suche".

In diesem Artikel werden die Strategien und Entscheidungskriterien für die schrittweise Skalierung von einer kleinen Einzelserver-Konfiguration bis hin zu einer großen Cluster-Konfiguration erläutert.

Zielgruppe
==========

- Personen, die einen großangelegten Fess-Betrieb planen
- Personen, die mit Leistungsproblemen konfrontiert sind
- Personen, die die grundlegenden Konzepte von OpenSearch-Clustern verstehen möchten

Skalierungsstufen
==================

Die Skalierung von Fess erfolgt typischerweise in den folgenden Stufen.

.. list-table:: Skalierungsstufen
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Stufe
     - Konfiguration
     - Dokumentenanzahl (ca.)
     - Benutzeranzahl (ca.)
     - Kosten
   * - S
     - Einzelserver
     - Bis zu 1 Million
     - Bis zu 50
     - Niedrig
   * - M
     - Getrennte Konfiguration
     - Bis zu 1 Million
     - Bis zu 500
     - Mittel
   * - L
     - Cluster-Konfiguration
     - 1 Million bis 10 Millionen
     - Bis zu mehrere Tausend
     - Hoch
   * - XL
     - Multi-Instanz
     - 10 Millionen oder mehr
     - Mehrere Tausend oder mehr
     - Am höchsten

Stufe S: Einzelserver-Konfiguration
=====================================

Dies entspricht der in Teil 2 erstellten Docker Compose-Konfiguration.
Fess und OpenSearch laufen auf demselben Server.

Einsatzszenarien
-----------------

- Ersteinrichtung, PoC, kleine bis mittelgroße Organisationen
- Dokumentenanzahl von 1 Million oder weniger
- Wenige gleichzeitige Suchbenutzer

Tuning-Punkte
--------------

**JVM-Heap-Anpassung**

Stellen Sie die JVM-Heap-Größe für Fess und OpenSearch jeweils angemessen ein.

- Fess: Maximal 2 GB (Standard; anfänglicher Heap beträgt 256 MB)
- OpenSearch: 50 % oder weniger des physischen Speichers, jedoch nicht mehr als 32 GB

**Thread-Pool**

Passen Sie die Anzahl der Crawl-Threads entsprechend der CPU-Kernanzahl des Servers an.

Stufe M: Getrennte Konfiguration
==================================

Trennen Sie den Fess-Server und den OpenSearch-Server physisch.

Einsatzszenarien
-----------------

- Wenn die Anzahl gleichzeitiger Suchbenutzer steigt und die Suchleistung während des Crawlings zum Problem wird
- Wenn Arbeitsspeicher oder CPU in Stufe S knapp werden

Konfiguration
--------------

::

    [Fess-Server] <-> [OpenSearch-Server]

Ändern Sie in den Fess-Einstellungen das OpenSearch-Verbindungsziel auf den externen Server.

Vorteile
---------

- Beseitigung der Ressourcenkonflikte zwischen Fess (Crawl-Verarbeitung) und OpenSearch (Suchverarbeitung)
- Optimale Ressourcenzuweisung (CPU, Arbeitsspeicher) für jeden Server möglich
- Unabhängige Festplatten-I/O des OpenSearch-Servers

Stufe L: Cluster-Konfiguration
================================

Konfigurieren Sie OpenSearch als Cluster, um die Suchredundanz und Leistung zu verbessern.

Einsatzszenarien
-----------------

- Dokumentenanzahl von 1 Million bis 10 Millionen
- Wenn hohe Verfügbarkeit erforderlich ist
- Wenn die Verbesserung der Suchantwortzeiten notwendig ist

Konfigurationsbeispiel
-----------------------

::

    [Fess-Server]
          |
    [OpenSearch-Knoten 1] (Master/Daten)
    [OpenSearch-Knoten 2] (Daten)
    [OpenSearch-Knoten 3] (Daten)

Der OpenSearch-Cluster verteilt und repliziert Daten mithilfe der Konzepte von Shards und Replicas.

**Shards**: Aufteilen des Index und Verteilung auf mehrere Knoten (schnellere Verarbeitung durch Parallelisierung)

**Replicas**: Aufbewahrung von Shard-Kopien auf anderen Knoten (Redundanz bei Ausfällen + Parallelisierung der Suche)

Konfigurationshinweise
-----------------------

- Anzahl der Shards: Entsprechend der Dokumentenanzahl und Suchleistung einstellen (Richtwert: 10-50 GB pro Shard)
- Anzahl der Replicas: Mindestens 1 (zur Sicherstellung der Redundanz)
- Anzahl der Knoten: Mindestens 3 (Quorum für die Master-Wahl)

Stufe XL: Multi-Instanz-Konfiguration
=======================================

Konfigurieren Sie mehrere Fess-Instanzen, um die Crawl- und Suchverarbeitung zu verteilen.

Einsatzszenarien
-----------------

- Dokumentenanzahl übersteigt 10 Millionen
- Große Crawl-Jobs müssen parallel ausgeführt werden
- Hochfrequente Suchanfragen

Konfigurationsbeispiel
-----------------------

::

    [Load Balancer]
      +-- [Fess-Instanz 1] (Suche + Verwaltung)
      +-- [Fess-Instanz 2] (Suche)
      +-- [Fess-Instanz 3] (Nur Crawling)
              |
    [OpenSearch-Cluster]
      +-- [Knoten 1] (Master)
      +-- [Knoten 2] (Daten)
      +-- [Knoten 3] (Daten)
      +-- [Knoten 4] (Daten)

Ab Fess 15.6 ermöglicht die Funktion für verteilte Koordination die exklusive Steuerung von Wartungsoperationen (wie Indexneuaufbau und -leerung) über mehrere Fess-Instanzen hinweg.

Entscheidungsflussdiagramm für die Skalierung
================================================

Wenn Leistungsprobleme auftreten, identifizieren Sie die Ursache und erwägen Sie Gegenmaßnahmen in der folgenden Reihenfolge.

**1. Wenn die Suche langsam ist**

- Überprüfen Sie den OpenSearch-Clusterstatus
- Überprüfen Sie die JVM-Heap-Auslastung
- Überprüfen Sie die Indexgröße
- -> Stufe M (Trennung) oder Stufe L (Clustering) in Betracht ziehen

**2. Wenn das Crawling langsam ist oder nicht abgeschlossen wird**

- Überprüfen Sie die Anzahl der zu crawlenden Dokumente
- Passen Sie die Thread-Anzahl und das Intervall an
- Überprüfen Sie die Auswirkungen auf die Suche während des Crawlings
- -> Stufe M (Trennung) oder Stufe XL (dedizierte Crawl-Instanz) in Betracht ziehen

**3. Wenn viele gleichzeitige Zugriffe vorliegen**

- Überwachen Sie die Suchantwortzeiten
- Überprüfen Sie die CPU-Auslastung des Fess-Servers
- -> Stufe XL (Load Balancer + mehrere Instanzen) in Betracht ziehen

JVM-Tuning
============

In jeder Stufe hat das JVM-Tuning einen erheblichen Einfluss auf die Leistung.

Wichtige Parameter
-------------------

.. list-table:: JVM-Parameter
   :header-rows: 1
   :widths: 25 35 40

   * - Parameter
     - Beschreibung
     - Empfohlener Wert
   * - ``-Xmx``
     - Maximale Heap-Größe
     - 50 % oder weniger des physischen Speichers
   * - ``-Xms``
     - Anfängliche Heap-Größe
     - Gleicher Wert wie ``-Xmx``
   * - GC-Einstellungen
     - Garbage-Collection-Methode
     - G1GC (Standard)

Richtwerte für die Heap-Größe
----------------------------------

- 1 Million oder weniger: 2-4 GB
- 1 Million bis 5 Millionen: 8 GB
- 5 Millionen bis 10 Millionen: 16 GB
- 10 Millionen oder mehr: 32 GB oder mehr (OpenSearch-Seite)

Zusammenfassung
================

In diesem Artikel wurden die schrittweisen Skalierungsstrategien für Fess erläutert.

- **Stufe S**: Einzelserver (bis zu 1 Million Dokumente)
- **Stufe M**: Fess / OpenSearch-Trennung (bis zu 1 Million Dokumente, Unterstützung mehrerer Benutzer)
- **Stufe L**: OpenSearch-Clustering (1 Million bis 10 Millionen Dokumente)
- **Stufe XL**: Fess Multi-Instanz (10 Millionen Dokumente oder mehr)
- Entscheidungsflussdiagramm für die Skalierung und JVM-Tuning

Mit dem Ansatz "klein anfangen und bei Bedarf wachsen" können Sie entsprechend den Anforderungen skalieren und dabei die Kosten unter Kontrolle halten.

Im nächsten Artikel wird die Sicherheitsarchitektur behandelt.

Referenzen
==========

- `Fess Installationshandbuch <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `OpenSearch-Cluster-Konfiguration <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
