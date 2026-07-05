==================================
Rank Fusion Konfiguration
==================================

Übersicht
=========

Die Rank Fusion-Funktion von |Fess| integriert mehrere Suchergebnisse,
um genauere Suchergebnisse zu liefern.

Was ist Rank Fusion
====================

Rank Fusion ist eine Technik, die Ergebnisse aus mehreren Suchalgorithmen
oder Bewertungsmethoden kombiniert, um ein einzelnes optimiertes Ranking zu generieren.

Hauptvorteile:

- Kombiniert die Stärken verschiedener Algorithmen
- Verbessert die Suchgenauigkeit
- Liefert vielfältige Suchergebnisse

Unterstützte Algorithmen
=========================

|Fess| unterstützt den RRF (Reciprocal Rank Fusion)-Algorithmus für Rank Fusion.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF berechnet einen Score durch Summierung des Kehrwerts der Rangposition
jedes Dokuments in jedem Suchergebnis. Wenn ein Dokument von mehreren Suchern
abgerufen wird, werden seine Scores addiert.

Formel::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Konstanter Parameter, der den Einfluss des Rangs steuert (Standard: 20)
- ``rank(d)``: Rang des Dokuments d in jedem Suchergebnis (0-basiert)
- ``Σ``: Summe über alle Sucher, in denen Dokument d vorkommt

Einstellungen
=============

fess_config.properties
----------------------

Grundkonfiguration::

    # Fenstergröße (Anzahl der zu fusionierenden Ergebnisse)
    # Hinweis: Muss >= paging.search.page.max.size × 2 sein.
    # Wenn der Wert unter diesem Minimum liegt, wird das Minimum automatisch verwendet.
    rank.fusion.window_size=200

    # Rang-Konstante (k-Parameter für RRF)
    rank.fusion.rank_constant=20

    # Anzahl der Threads für parallele Verarbeitung
    # (bei 0 oder kleiner wird availableProcessors × 1.5 + 1 verwendet)
    rank.fusion.threads=-1

    # Name des Score-Felds (Feld, in dem der fusionierte Score gespeichert wird)
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Eigenschaft
     - Standard
     - Beschreibung
   * - ``rank.fusion.window_size``
     - ``200``
     - Maximale Anzahl der Ergebnisse, die von jedem Sucher für die Fusion abgerufen werden. Muss >= ``paging.search.page.max.size × 2`` (standardmäßig ``200``) sein; bei einem kleineren Wert wird dieser automatisch auf dieses Minimum angehoben.
   * - ``rank.fusion.rank_constant``
     - ``20``
     - Die Konstante ``k`` in der RRF-Formel. Ein größerer Wert verringert den Score-Unterschied zwischen höher und niedriger platzierten Ergebnissen.
   * - ``rank.fusion.threads``
     - ``-1``
     - Anzahl der Threads beim parallelen Ausführen mehrerer Sucher. Bei Angabe von ``0`` oder kleiner wird automatisch ``availableProcessors × 1.5 + 1`` verwendet.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Name des Ergebnisdokument-Felds, in dem der fusionierte Score gespeichert wird.

JVM-Systemeigenschaften
-----------------------

Die zu verwendenden Sucher werden als JVM-Systemeigenschaft angegeben. Fügen Sie Folgendes
zu ``fess.in.sh`` (oder ``fess.in.bat``) hinzu::

    # Sucher angeben (kommagetrennt)
    -Drank.fusion.searchers=default,semantic

Diese Eigenschaft verhält sich wie folgt:

- Sie wird als JVM-Option gesetzt, nicht in ``fess_config.properties``.
- ``default`` ist der Sucher, der die Standard-Schlüsselwortsuche ausführt, und ist stets verfügbar.
- ``semantic`` ist der Sucher, der die semantische Suche (Vektorsuche) ausführt, und ist verfügbar, wenn das Semantic Search-Plugin (``fess-webapp-semantic-search``) installiert ist.
- Wird diese Eigenschaft nicht angegeben, werden alle registrierten Sucher verwendet. Stimmt keiner der angegebenen Namen mit einem registrierten Sucher überein, wird nur der ``default``-Sucher verwendet.
- Die Ergebnisfusion durch Rank Fusion wird nur ausgeführt, wenn zwei oder mehr Sucher verfügbar sind. Bei nur einem verfügbaren Sucher wird keine Fusion durchgeführt und normale Suchergebnisse werden zurückgegeben.

Integration mit Hybridsuche
============================

Rank Fusion ist besonders effektiv bei der Hybridsuche, die Schlüsselwortsuche
und semantische Suche kombiniert. Um die semantische Suche zu nutzen, installieren
Sie das Semantic Search-Plugin (``fess-webapp-semantic-search``) und fügen Sie
``semantic`` zu ``-Drank.fusion.searchers`` hinzu.

Anwendungsbeispiele
===================

Grundlegende Hybridsuche
------------------------

1. BM25-Score mit Schlüsselwortsuche berechnen
2. Vektorähnlichkeit mit semantischer Suche berechnen
3. Beide Ergebnisse mit RRF fusionieren
4. Endgültiges Ranking generieren

Suchablauf::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

Leistungsüberlegungen
======================

Speicherverbrauch
-----------------

- Der Speicherverbrauch steigt, da mehrere Suchergebnisse vorgehalten werden.
- Verwenden Sie ``rank.fusion.window_size``, um die maximale Anzahl der zu fusionierenden Ergebnisse zu begrenzen. Der Hauptsucher (der führende ``default``-Sucher) ruft bis zu ``window_size`` Ergebnisse ab, während jeder der anderen Sucher ``window_size ÷ Anzahl der Sucher`` Ergebnisse abruft.

::

    # Fenstergröße für die Fusion
    rank.fusion.window_size=200

Verarbeitungszeit
-----------------

- Die Antwortzeit steigt, da mehrere Suchen ausgeführt werden.
- Verwenden Sie ``rank.fusion.threads``, um die Anzahl der Threads für die parallele Ausführung festzulegen.

::

    # Anzahl der Threads für parallele Ausführung
    # (bei 0 oder kleiner wird availableProcessors × 1.5 + 1 verwendet)
    rank.fusion.threads=-1

Fehlersuche
===========

Suchergebnisse weichen von Erwartungen ab
-----------------------------------------

**Symptom**: Ergebnisse nach Rank Fusion weichen von den Erwartungen ab

**Prüfpunkte**:

1. Ergebnisse jedes Suchtyps einzeln überprüfen
2. Den Wert von ``rank.fusion.rank_constant`` anpassen
3. Den Wert von ``rank.fusion.window_size`` anpassen
4. Bei tiefen Seiten (wo ``Startposition × 2`` größer oder gleich ``rank.fusion.window_size`` ist) wird keine Fusion durchgeführt und nur der Hauptsucher wird verwendet. Wenn Sie auf mehr Seiten fusionierte Ergebnisse wünschen, erhöhen Sie ``rank.fusion.window_size``.

Suche ist langsam
-----------------

**Symptom**: Suche wird bei aktiviertem Rank Fusion langsam

**Lösungen**:

1. ``rank.fusion.window_size`` reduzieren::

       rank.fusion.window_size=100

2. ``rank.fusion.threads`` anpassen::

       rank.fusion.threads=4

Speichermangel
--------------

**Symptom**: OutOfMemoryError tritt auf

**Lösungen**:

1. ``rank.fusion.window_size`` reduzieren
2. JVM-Heap-Größe erhöhen

Referenz
========

- :doc:`scripting-overview` - Scripting-Übersicht
- :doc:`search-advanced` - Erweiterte Sucheinstellungen
- :doc:`llm-overview` - LLM-Integrations-Leitfaden (Semantische Suche)
