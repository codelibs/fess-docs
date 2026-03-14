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

|Fess| unterstützt den RRF (Reciprocal Rank Fusion)-Algorithmus.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF berechnet Scores durch Summierung des Kehrwerts der Rangposition jedes Ergebnisses.

Formel::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Konstanter Parameter (Standard: 20)
- ``rank(d)``: Rang des Dokuments d in jedem Suchergebnis

Einstellungen
==============

fess_config.properties
----------------------

Grundeinstellungen::

    # Fenstergröße (Anzahl der Ergebnisse für die Fusion)
    rank.fusion.window_size=200

    # RRF rank_constant (k-Parameter)
    rank.fusion.rank_constant=20

    # Anzahl der Threads für parallele Verarbeitung (-1 ist Standard)
    rank.fusion.threads=-1

    # Name des Score-Felds
    rank.fusion.score_field=rf_score

Integration mit Hybridsuche
============================

Rank Fusion ist besonders effektiv bei der Hybridsuche, die Schlüsselwortsuche
und semantische Suche kombiniert.

Anwendungsbeispiele
====================

Grundlegende Hybridsuche
--------------------------

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
------------------

- Der Speicherverbrauch steigt, da mehrere Suchergebnisse gehalten werden
- Begrenzen Sie die maximale Anzahl der Fusionsziele mit ``rank.fusion.window_size``

::

    # Fenstergröße für die Fusion
    rank.fusion.window_size=200

Verarbeitungszeit
------------------

- Die Antwortzeit steigt, da mehrere Suchen ausgeführt werden
- Setzen Sie die Anzahl der Threads für parallele Ausführung mit ``rank.fusion.threads``

::

    # Anzahl der Threads für parallele Ausführung (-1 ist Standard)
    rank.fusion.threads=-1

Fehlersuche
============

Suchergebnisse weichen von Erwartungen ab
-------------------------------------------

**Symptom**: Ergebnisse nach Rank Fusion weichen von den Erwartungen ab

**Prüfpunkte**:

1. Ergebnisse jedes Suchtyps einzeln überprüfen
2. Den ``rank.fusion.rank_constant``-Wert anpassen
3. Den ``rank.fusion.window_size``-Wert anpassen

Suche ist langsam
------------------

**Symptom**: Suche wird bei aktiviertem Rank Fusion langsam

**Lösungen**:

1. ``rank.fusion.window_size`` reduzieren::

       rank.fusion.window_size=100

2. ``rank.fusion.threads`` anpassen::

       rank.fusion.threads=4

Speichermangel
---------------

**Symptom**: OutOfMemoryError tritt auf

**Lösungen**:

1. ``rank.fusion.window_size`` reduzieren
2. JVM-Heap-Größe erhöhen

Referenz
========

- :doc:`scripting-overview` - Scripting-Übersicht
- :doc:`../admin/search-settings` - Sucheinstellungen-Leitfaden
- :doc:`llm-overview` - LLM-Integrations-Leitfaden (Semantische Suche)
