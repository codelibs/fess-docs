============================================================
Teil 14: Skalierungsstrategien fuer Suchsysteme -- Schrittweise Erweiterung von klein zu gross
============================================================

Einfuehrung
============

Wenn Sie Fess zunachst in kleinem Umfang einfuehren, entstehen mit wachsender Nutzung unweigerlich Anforderungen wie "mehr Dokumente", "mehr Benutzer" und "schnellere Suche".

In diesem Artikel werden die Strategien und Entscheidungskriterien fuer die schrittweise Skalierung von einer kleinen Einzelserver-Konfiguration bis hin zu einer grossen Cluster-Konfiguration erlaeutert.

Zielgruppe
==========

- Personen, die einen grossangelegten Fess-Betrieb planen
- Personen, die mit Leistungsproblemen konfrontiert sind
- Personen, die die grundlegenden Konzepte von OpenSearch-Clustern verstehen moechten

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
     - Am hoechsten

Stufe S: Einzelserver-Konfiguration
=====================================

Dies entspricht der in Teil 2 erstellten Docker Compose-Konfiguration.
Fess und OpenSearch laufen auf demselben Server.

Einsatzszenarien
-----------------

- Ersteinrichtung, PoC, kleine bis mittelgrosse Organisationen
- Dokumentenanzahl von 1 Million oder weniger
- Wenige gleichzeitige Suchbenutzer

Tuning-Punkte
--------------

**JVM-Heap-Anpassung**

Stellen Sie die JVM-Heap-Groesse fuer Fess und OpenSearch jeweils angemessen ein.

- Fess: Maximal 2 GB (Standard; anfaenglicher Heap betraegt 256 MB)
- OpenSearch: 50 % oder weniger des physischen Speichers, jedoch nicht mehr als 32 GB

**Thread-Pool**

Passen Sie die Anzahl der Crawl-Threads entsprechend der CPU-Kernanzahl des Servers an.

Stufe M: Getrennte Konfiguration
==================================

Trennen Sie den Fess-Server und den OpenSearch-Server physisch.

Einsatzszenarien
-----------------

- Wenn die Anzahl gleichzeitiger Suchbenutzer steigt und die Suchleistung waehrend des Crawlings zum Problem wird
- Wenn Arbeitsspeicher oder CPU in Stufe S knapp werden

Konfiguration
--------------

::

    [Fess-Server] <-> [OpenSearch-Server]

Aendern Sie in den Fess-Einstellungen das OpenSearch-Verbindungsziel auf den externen Server.

Vorteile
---------

- Beseitigung der Ressourcenkonflikte zwischen Fess (Crawl-Verarbeitung) und OpenSearch (Suchverarbeitung)
- Optimale Ressourcenzuweisung (CPU, Arbeitsspeicher) fuer jeden Server moeglich
- Unabhaengige Festplatten-I/O des OpenSearch-Servers

Stufe L: Cluster-Konfiguration
================================

Konfigurieren Sie OpenSearch als Cluster, um die Suchredundanz und Leistung zu verbessern.

Einsatzszenarien
-----------------

- Dokumentenanzahl von 1 Million bis 10 Millionen
- Wenn hohe Verfuegbarkeit erforderlich ist
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

**Replicas**: Aufbewahrung von Shard-Kopien auf anderen Knoten (Redundanz bei Ausfaellen + Parallelisierung der Suche)

Konfigurationshinweise
-----------------------

- Anzahl der Shards: Entsprechend der Dokumentenanzahl und Suchleistung einstellen (Richtwert: 10-50 GB pro Shard)
- Anzahl der Replicas: Mindestens 1 (zur Sicherstellung der Redundanz)
- Anzahl der Knoten: Mindestens 3 (Quorum fuer die Master-Wahl)

Stufe XL: Multi-Instanz-Konfiguration
=======================================

Konfigurieren Sie mehrere Fess-Instanzen, um die Crawl- und Suchverarbeitung zu verteilen.

Einsatzszenarien
-----------------

- Dokumentenanzahl uebersteigt 10 Millionen
- Grosse Crawl-Jobs muessen parallel ausgefuehrt werden
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

Ab Fess 15.6 ermoeglicht die Funktion fuer verteilte Koordination die exklusive Steuerung von Wartungsoperationen (wie Indexneuaufbau und -leerung) ueber mehrere Fess-Instanzen hinweg.

Entscheidungsflussdiagramm fuer die Skalierung
================================================

Wenn Leistungsprobleme auftreten, identifizieren Sie die Ursache und erwaegen Sie Gegenmassnahmen in der folgenden Reihenfolge.

**1. Wenn die Suche langsam ist**

- Ueberpruefen Sie den OpenSearch-Clusterstatus
- Ueberpruefen Sie die JVM-Heap-Auslastung
- Ueberpruefen Sie die Indexgroesse
- -> Stufe M (Trennung) oder Stufe L (Clustering) in Betracht ziehen

**2. Wenn das Crawling langsam ist oder nicht abgeschlossen wird**

- Ueberpruefen Sie die Anzahl der zu crawlenden Dokumente
- Passen Sie die Thread-Anzahl und das Intervall an
- Ueberpruefen Sie die Auswirkungen auf die Suche waehrend des Crawlings
- -> Stufe M (Trennung) oder Stufe XL (dedizierte Crawl-Instanz) in Betracht ziehen

**3. Wenn viele gleichzeitige Zugriffe vorliegen**

- Ueberwachen Sie die Suchantwortzeiten
- Ueberpruefen Sie die CPU-Auslastung des Fess-Servers
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
     - Maximale Heap-Groesse
     - 50 % oder weniger des physischen Speichers
   * - ``-Xms``
     - Anfaengliche Heap-Groesse
     - Gleicher Wert wie ``-Xmx``
   * - GC-Einstellungen
     - Garbage-Collection-Methode
     - G1GC (Standard)

Richtwerte fuer die Heap-Groesse
----------------------------------

- 1 Million oder weniger: 2-4 GB
- 1 Million bis 5 Millionen: 8 GB
- 5 Millionen bis 10 Millionen: 16 GB
- 10 Millionen oder mehr: 32 GB oder mehr (OpenSearch-Seite)

Zusammenfassung
================

In diesem Artikel wurden die schrittweisen Skalierungsstrategien fuer Fess erlaeutert.

- **Stufe S**: Einzelserver (bis zu 1 Million Dokumente)
- **Stufe M**: Fess / OpenSearch-Trennung (bis zu 1 Million Dokumente, Unterstuetzung mehrerer Benutzer)
- **Stufe L**: OpenSearch-Clustering (1 Million bis 10 Millionen Dokumente)
- **Stufe XL**: Fess Multi-Instanz (10 Millionen Dokumente oder mehr)
- Entscheidungsflussdiagramm fuer die Skalierung und JVM-Tuning

Mit dem Ansatz "klein anfangen und bei Bedarf wachsen" koennen Sie entsprechend den Anforderungen skalieren und dabei die Kosten unter Kontrolle halten.

Im naechsten Artikel wird die Sicherheitsarchitektur behandelt.

Referenzen
==========

- `Fess Installationshandbuch <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `OpenSearch-Cluster-Konfiguration <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
