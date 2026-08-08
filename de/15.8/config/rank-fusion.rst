============================================================
Hybride Suche und Rank Fusion (Semantisch + Schlüsselwort)
============================================================

Übersicht
=========

**Hybride Suche** in |Fess| kombiniert die klassische Schlüsselwortsuche (BM25) mit **semantischer (Vektor-)Suche** und führt beide Ergebnismengen mit **Rank Fusion** zu präziseren, relevanteren Rankings zusammen. Rank Fusion integriert die Ergebnisse mehrerer Sucher zu einem einzigen optimierten Ranking.

In |Fess| 15.8 wird die semantische Suche (Content-Chunking + Vektorsuche) als Kernfunktion
bereitgestellt. Sobald Sie sie aktivieren, wird der semantische Sucher automatisch bei Rank Fusion
registriert. Siehe :doc:`search-semantic` zur Konfiguration.

Die Rank Fusion-Funktion von |Fess| integriert mehrere Suchergebnisse,
um genauere Suchergebnisse zu liefern.

Was ist Rank Fusion
====================

Rank Fusion ist eine Technik, die Ergebnisse aus mehreren Suchalgorithmen
oder Bewertungsmethoden (zum Beispiel Schlüsselwort-/BM25- und semantische/Vektor-Suche) kombiniert, um ein einzelnes optimiertes Ranking zu generieren.

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
    # (bei 0 oder kleiner wird die Anzahl verfügbarer CPU-Kerne × 1.5 + 1 verwendet)
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
     - Anzahl der Threads beim parallelen Ausführen mehrerer Sucher. Bei Angabe von ``0`` oder kleiner wird automatisch ``Anzahl verfügbarer CPU-Kerne × 1.5 + 1`` verwendet.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Name des Ergebnisdokument-Felds, in dem der fusionierte Score gespeichert wird.

JVM-Systemeigenschaften
-----------------------

Die zu verwendenden Sucher werden als JVM-Systemeigenschaft angegeben. Fügen Sie Folgendes
zu ``fess.in.sh`` (oder ``fess.in.bat``) hinzu::

    # Sucher angeben (kommagetrennt)
    -Drank.fusion.searchers=default,semantic_chunk

Diese Eigenschaft verhält sich wie folgt:

- Sie wird als JVM-Option gesetzt, nicht in ``fess_config.properties``.
- ``default`` ist der Sucher, der die Standard-Schlüsselwortsuche ausführt, und ist stets verfügbar.
- Der Name eines Suchers leitet sich vom Namen seiner Implementierungsklasse ab: Das abschließende
  ``Searcher`` wird entfernt und der Rest in Snake Case in Kleinbuchstaben umgewandelt
  (``SemanticChunkSearcher`` → ``semantic_chunk``). Der im Kern integrierte semantische Sucher
  (:doc:`search-semantic`) wird unter dem Namen ``semantic_chunk`` registriert.
- Wird diese Eigenschaft nicht angegeben, werden alle registrierten Sucher verwendet. Stimmt keiner der angegebenen Namen mit einem registrierten Sucher überein, wird nur der ``default``-Sucher verwendet. Wenn Sie den im Kern integrierten semantischen Sucher (:doc:`search-semantic`) verwenden, müssen Sie diese Eigenschaft normalerweise überhaupt nicht setzen.
- Die Ergebnisfusion durch Rank Fusion wird nur ausgeführt, wenn zwei oder mehr Sucher verfügbar sind. Bei nur einem verfügbaren Sucher wird keine Fusion durchgeführt und normale Suchergebnisse werden zurückgegeben.

.. warning::

   Wenn Sie zuvor das Plugin ``fess-webapp-semantic-search`` aus |Fess| 15.7 oder früher genutzt
   haben, wurde Ihnen möglicherweise empfohlen, diese Eigenschaft auf
   ``-Drank.fusion.searchers=default,semantic`` zu setzen. Dieses Plugin registrierte seinen
   Sucher unter dem Namen ``semantic``, was ein **anderer Sucher** ist als der in 15.8 eingeführte
   Name des im Kern integrierten Suchers, ``semantic_chunk``. Wenn Sie diese Einstellung aus der
   15.7-Ära unverändert nach 15.8 übernehmen, enthält die Allowlist niemals ``semantic_chunk``,
   sodass die im Kern integrierte semantische Suche (Content-Chunking + Vektorsuche) **überhaupt
   nicht funktioniert** — |Fess| liefert stillschweigend weiterhin gewöhnliche
   Schlüsselwortsuchergebnisse (beim Start wird zwar eine Warnung protokolliert, aber der
   Ausschluss pro Anfrage selbst wird nur auf DEBUG-Ebene protokolliert). Wenn Ihre Konfiguration
   ``default,semantic`` angibt, entfernen Sie diese Einstellung entweder oder fügen Sie
   ``semantic_chunk`` hinzu. Siehe „Migration von 15.7 oder früheren Versionen" in
   :doc:`search-semantic` für Details.

Integration mit Hybridsuche
============================

Rank Fusion ist besonders effektiv bei der Hybridsuche, die Schlüsselwortsuche
und semantische Suche kombiniert. Um die semantische Suche zu nutzen, konfigurieren Sie die
Content-Chunking-Funktion und setzen Sie ``content_chunker.search.enabled=true``. Siehe
:doc:`search-semantic` für Details.

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
    # (bei 0 oder kleiner wird die Anzahl verfügbarer CPU-Kerne × 1.5 + 1 verwendet)
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
