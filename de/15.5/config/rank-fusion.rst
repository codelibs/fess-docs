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

|Fess| unterstützt die folgenden Rank Fusion-Algorithmen:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Algorithmus
     - Beschreibung
   * - RRF (Reciprocal Rank Fusion)
     - Fusionsalgorithmus basierend auf dem Kehrwert der Rangposition
   * - Score Fusion
     - Fusion durch Score-Normalisierung und gewichteten Durchschnitt
   * - Borda Count
     - Abstimmungsbasierte Ranking-Fusion

RRF (Reciprocal Rank Fusion)
----------------------------

RRF berechnet Scores durch Summierung des Kehrwerts der Rangposition jedes Ergebnisses.

Formel::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Konstanter Parameter (Standard: 60)
- ``rank(d)``: Rang des Dokuments d in jedem Suchergebnis

Einstellungen
==============

fess_config.properties
----------------------

Grundeinstellungen::

    # Rank Fusion aktivieren
    rank.fusion.enabled=true

    # Zu verwendender Algorithmus
    rank.fusion.algorithm=rrf

    # RRF k-Parameter
    rank.fusion.rrf.k=60

    # Suchtypen für die Fusion
    rank.fusion.search.types=keyword,semantic

Algorithmus-spezifische Einstellungen
--------------------------------------

RRF-Einstellungen::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Score Fusion-Einstellungen::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Borda Count-Einstellungen::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

Integration mit Hybridsuche
============================

Rank Fusion ist besonders effektiv bei der Hybridsuche, die Schlüsselwortsuche
und semantische Suche kombiniert.

Konfigurationsbeispiel
-----------------------

::

    # Hybridsuche aktivieren
    search.hybrid.enabled=true

    # Ergebnisse von Schlüsselwortsuche und semantischer Suche fusionieren
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # Gewichtung für jeden Suchtyp
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

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

Benutzerdefiniertes Scoring
----------------------------

Beispiel für die Kombination mehrerer Score-Faktoren::

    # Basis-Suchscore + Datums-Boost + Popularität
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

Leistungsüberlegungen
======================

Speicherverbrauch
------------------

- Der Speicherverbrauch steigt, da mehrere Suchergebnisse gehalten werden
- Begrenzen Sie die maximale Anzahl der Fusionsziele mit ``rank.fusion.max.results``

::

    # Maximale Ergebnisanzahl für die Fusion
    rank.fusion.max.results=1000

Verarbeitungszeit
------------------

- Die Antwortzeit steigt, da mehrere Suchen ausgeführt werden
- Erwägen Sie Optimierung durch parallele Ausführung

::

    # Parallele Ausführung aktivieren
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

Cache
------

- Nutzen Sie Caching für häufige Abfragen

::

    # Cache für Rank Fusion-Ergebnisse
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

Fehlersuche
============

Suchergebnisse weichen von Erwartungen ab
-------------------------------------------

**Symptom**: Ergebnisse nach Rank Fusion weichen von den Erwartungen ab

**Prüfpunkte**:

1. Ergebnisse jedes Suchtyps einzeln überprüfen
2. Prüfen, ob die Gewichtung angemessen ist
3. Den k-Parameterwert anpassen

Suche ist langsam
------------------

**Symptom**: Suche wird bei aktiviertem Rank Fusion langsam

**Lösungen**:

1. Parallele Ausführung aktivieren::

       rank.fusion.parallel=true

2. Anzahl der Fusionsziel-Ergebnisse begrenzen::

       rank.fusion.max.results=500

3. Caching aktivieren::

       rank.fusion.cache.enabled=true

Speichermangel
---------------

**Symptom**: OutOfMemoryError tritt auf

**Lösungen**:

1. Maximale Anzahl der Fusionsziel-Ergebnisse reduzieren
2. JVM-Heap-Größe erhöhen
3. Nicht benötigte Suchtypen deaktivieren

Referenz
========

- :doc:`scripting-overview` - Scripting-Übersicht
- :doc:`../admin/search-settings` - Sucheinstellungen-Leitfaden
- :doc:`llm-overview` - LLM-Integrations-Leitfaden (Semantische Suche)
