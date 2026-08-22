============================================================
Hybride Suche und Rank Fusion (Semantisch + Schlüsselwort)
============================================================

Übersicht
=========

**Hybride Suche** in |Fess| kombiniert die klassische Schlüsselwortsuche (BM25) mit **semantischer (Vektor-)Suche** und führt beide Ergebnismengen mit **Rank Fusion** zu präziseren, relevanteren Rankings zusammen. Rank Fusion integriert die Ergebnisse mehrerer Sucher zu einem einzigen optimierten Ranking.

In |Fess| 15.9 wird die semantische Suche (Content-Chunking + Vektorsuche) als Kernfunktion
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

.. note::

   Der Fusionsalgorithmus ist fest auf RRF eingestellt; es gibt keine Einstellung, um auf einen
   anderen Algorithmus umzuschalten. Ebenso wird keine Gewichtung einzelner Sucher unterstützt —
   der Beitrag jedes Suchers geht mit demselben Gewicht in die Summe ein. Die einzige
   Stellschraube für die Ranking-Tendenz ist ``rank.fusion.rank_constant``.

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
    # (bei 0 oder kleiner wird die Anzahl verfügbarer CPU-Kerne × 3 ÷ 2 + 1 verwendet)
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
     - Maximale Anzahl der Ergebnisse, die von jedem Sucher für die Fusion abgerufen werden. Muss >= ``paging.search.page.max.size × 2`` (standardmäßig ``200``) sein; bei einem kleineren Wert wird dieser automatisch auf dieses Minimum angehoben (beim Start wird dazu eine WARN-Meldung protokolliert).
   * - ``rank.fusion.rank_constant``
     - ``20``
     - Die Konstante ``k`` in der RRF-Formel. Ein größerer Wert verringert den Score-Unterschied zwischen höher und niedriger platzierten Ergebnissen.
   * - ``rank.fusion.threads``
     - ``-1``
     - Anzahl der Threads des festen Thread-Pools, der mehrere Sucher parallel ausführt. Bei Angabe von ``0`` oder kleiner wird automatisch ``Anzahl verfügbarer CPU-Kerne × 3 ÷ 2 + 1`` verwendet (die Berechnung erfolgt in Ganzzahlarithmetik, Nachkommastellen werden also abgeschnitten; Beispiel: 4 Kerne → 7, 5 Kerne → 8).
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Name des Ergebnisdokument-Felds, in dem der fusionierte Score gespeichert wird.

.. note::

   **Wann Änderungen wirksam werden**

   Alle vier oben genannten Einstellungen erfordern einen Neustart von |Fess|, damit eine
   Änderung wirksam wird. Aus ``fess_config.properties`` gelesene Werte werden innerhalb der JVM
   zwischengespeichert; ein Bearbeiten der Datei im laufenden Betrieb bleibt daher wirkungslos.

   Ergänzend: ``rank.fusion.window_size`` wird nur einmal beim Start gelesen,
   ``rank.fusion.threads`` beim Anlegen des Thread-Pools. Der Thread-Pool wird angelegt, sobald
   ein anderer Sucher als ``default`` (etwa der semantische Sucher) registriert wird; ist die
   semantische Suche deaktiviert, wird der Thread-Pool gar nicht erst angelegt.

JVM-Systemeigenschaften
-----------------------

Die zu verwendenden Sucher werden als JVM-Systemeigenschaft angegeben. Fügen Sie Folgendes
zu ``fess.in.sh`` hinzu::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

Bei ``fess.in.bat`` lautet der Eintrag wie folgt::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

Diese Eigenschaft verhält sich wie folgt:

- Sie wird als JVM-Option gesetzt, nicht in ``fess_config.properties``. Geben Sie als Schlüssel
  genau ``rank.fusion.searchers`` an. Die bei anderen Einstellungen gebräuchlichen Formen mit
  vorangestelltem ``-Dfess.config.`` oder ``-Dfess.system.`` (etwa
  ``-Dfess.config.rank.fusion.searchers``) werden nicht erkannt.
- Anstelle einer JVM-Option können Sie den Wert auch in der Verwaltungsoberfläche unter
  „System > Allgemein" im Feld „Systemeigenschaften" als einzelne Zeile eintragen, etwa
  ``rank.fusion.searchers=default,semantic_chunk``. Beachten Sie jedoch, dass ein Wert in diesem
  Feld nur angewendet wird, wenn noch keine gleichnamige Systemeigenschaft gesetzt ist. Eine
  Angabe per ``-D`` hat also Vorrang, und um einen bereits angewendeten Wert zu ändern, ist ein
  Neustart von |Fess| erforderlich.
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
   Sucher unter dem Namen ``semantic``, was ein **anderer Sucher** ist als der in 15.9 eingeführte
   Name des im Kern integrierten Suchers, ``semantic_chunk``. Wenn Sie diese Einstellung aus der
   15.7-Ära unverändert nach 15.9 übernehmen, enthält die Allowlist niemals ``semantic_chunk``,
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
Content-Chunking-Funktion und setzen Sie anschließend ``content_chunker.search.enabled=true``.

.. warning::

   Die Einstellungen unter ``content_chunker.*`` — etwa ``content_chunker.enabled`` oder
   ``content_chunker.search.enabled`` — sind **Systemeigenschaften** und gehören nicht in
   ``fess_config.properties``. Tragen Sie sie in ``conf/system.properties`` ein oder geben Sie
   sie als JVM-Option an, zum Beispiel
   ``-Dfess.system.content_chunker.search.enabled=true``. Einträge in
   ``fess_config.properties`` bleiben wirkungslos. Zudem wird
   ``content_chunker.search.enabled`` nur beim Start ausgewertet; nach dem Aktivieren ist daher
   ein Neustart von |Fess| erforderlich.

Siehe :doc:`search-semantic` für Details.

Fusionsergebnisse überprüfen
============================

Ob Rank Fusion tatsächlich arbeitet, erkennen Sie an den beiden folgenden Feldern, die den
Suchergebnissen hinzugefügt werden.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feld
     - Inhalt
   * - ``searcher``
     - Array mit den Namen der Sucher, die dieses Dokument abgerufen haben (Beispiel: ``["default", "semantic_chunk"]``). Sind beide enthalten, wurde das Dokument sowohl von der Schlüsselwortsuche als auch von der semantischen Suche gefunden.
   * - ``rf_score``
     - Der mit RRF berechnete fusionierte Score. Der Feldname lässt sich über ``rank.fusion.score_field`` ändern.

Beide Werte werden zur Suchzeit dynamisch hinzugefügt und nicht im Index gespeichert.
Da sie standardmäßig nicht in der Antwort von ``/api/v2/search`` enthalten sind, nehmen Sie zum
Überprüfen die folgende Einstellung in ``fess_config.properties`` vor und starten Sie |Fess|
neu::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` fügt der Allowlist der Felder Einträge hinzu, die in
   der Antwort der v2-Such-API enthalten sein dürfen. Nehmen Sie dort keine Felder der
   Zugriffskontrolle wie ``role`` oder ``virtual_host`` auf, da sonst Informationen zur
   Zugriffskontrolle in der Antwort der Such-API offengelegt werden.

Auswirkungen auf die Trefferzahl
================================

Wird Rank Fusion ausgeführt, entspricht die zurückgegebene Gesamttrefferzahl nicht unverändert
der Trefferzahl des Hauptsuchers (des an erster Stelle registrierten ``default``-Suchers),
sondern wird wie folgt korrigiert::

    Gesamttrefferzahl = Gesamttrefferzahl des Hauptsuchers + Korrekturwert

Der Korrekturwert ist die Anzahl derjenigen Dokumente unter den obersten ``window_size ÷ 2``
Ergebnissen nach der Fusion, die nicht in den obersten ``window_size ÷ 2`` Ergebnissen des
Hauptsuchers enthalten waren. Die Trefferzahl erhöht sich also genau um die Dokumente, die nur
die semantische Suche gefunden hat.
Daher kann sich die Trefferzahl bei derselben Anfrage unterscheiden, je nachdem, ob die
Hybridsuche aktiviert ist oder nicht.

Wird die Gesamttrefferzahl des Hauptsuchers als Näherungswert (Untergrenze) zurückgegeben,
findet diese Korrektur nicht statt.

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
- Verwenden Sie ``rank.fusion.window_size``, um die maximale Anzahl der zu fusionierenden Ergebnisse zu begrenzen. Der Hauptsucher (der führende ``default``-Sucher) ruft bis zu ``window_size`` Ergebnisse ab, während jeder der anderen Sucher ``window_size ÷ Anzahl der Sucher`` Ergebnisse abruft (die ``Anzahl der Sucher`` ist die Gesamtzahl einschließlich des Hauptsuchers, und die Division wird abgerundet).
- Gibt es beispielsweise zwei Sucher (``default`` und ``semantic_chunk``) und gilt ``window_size=200``, so ruft der Hauptsucher 200 und der semantische Sucher 100 Ergebnisse ab; es werden also maximal 300 Dokumente vorgehalten.

::

    # Fenstergröße für die Fusion
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` kann ``paging.search.page.max.size × 2`` nicht unterschreiten.
   Steht ``paging.search.page.max.size`` auf dem Standardwert ``100``, liegt die Untergrenze bei
   ``200`` und damit genau beim Standardwert von ``rank.fusion.window_size``. Das bedeutet: **In
   der Standardkonfiguration lässt sich window_size gar nicht unter den Standardwert senken.**
   Ein kleinerer Wert führt beim Start lediglich zu einer WARN-Meldung und wird auf ``200``
   angehoben. Um den Wert tatsächlich zu verringern, müssen Sie zuerst
   ``paging.search.page.max.size`` senken; damit sinkt jedoch zugleich die maximale Anzahl an
   Ergebnissen, die im Suchbildschirm oder über die API pro Seite angefordert werden kann.

Verarbeitungszeit
-----------------

- Die Antwortzeit steigt, da mehrere Suchen ausgeführt werden.
- Verwenden Sie ``rank.fusion.threads``, um die Anzahl der Threads für die parallele Ausführung festzulegen.

::

    # Anzahl der Threads für parallele Ausführung
    # (bei 0 oder kleiner wird die Anzahl verfügbarer CPU-Kerne × 3 ÷ 2 + 1 verwendet)
    rank.fusion.threads=-1

.. note::

   Für die Ausführung der Sucher ist kein Timeout konfiguriert. Antwortet ein Sucher nicht,
   wartet die Suchanfrage, bis dieser abgeschlossen ist.

Verhalten bei Fehlern eines Suchers
===================================

Schlägt einer der Sucher mit einer Ausnahme fehl, wird sein Ergebnis als leer behandelt; es wird
eine WARN-Meldung protokolliert und die Fusion mit den Ergebnissen der übrigen Sucher
fortgesetzt. Die Suchanfrage selbst schlägt dadurch nicht fehl.

Ausgenommen davon sind Syntaxfehler in der Anfrage (``InvalidQueryException``) und das
Überschreiten der Paging-Obergrenze (``ResultOffsetExceededException``) — diese werden
unverändert als Fehler zurückgegeben. Zudem wird bei tiefen Seiten, auf denen keine Fusion
durchgeführt wird (wo ``Startposition × 2`` größer oder gleich ``rank.fusion.window_size`` ist),
eine im Hauptsucher aufgetretene Ausnahme unverändert als Fehler der Suchanfrage
zurückgegeben.

Kann der semantische Sucher den Embedding-Anbieter nicht erreichen oder schlägt die
Embedding-Verarbeitung fehl, gibt er ein leeres Ergebnis zurück. Auch in diesem Fall tritt kein
Fehler auf; zurückgegeben werden dann nur die Ergebnisse der Schlüsselwortsuche.

Fehlersuche
===========

Suchergebnisse weichen von Erwartungen ab
-----------------------------------------

**Symptom**: Ergebnisse nach Rank Fusion weichen von den Erwartungen ab

**Prüfpunkte**:

1. Prüfen Sie das Feld ``searcher`` (siehe „Fusionsergebnisse überprüfen"). Enthält es bei allen
   Dokumenten nur ``["default"]``, liefert der semantische Sucher keine Ergebnisse.
2. Prüfen Sie, ob die semantische Suche übersprungen wird. Neben Anfragen, die Suchsyntax
   enthalten (etwa ``"``, ``:`` oder ``AND``), liefert der semantische Sucher auch beim
   Eingrenzen über Labels, Sortierung oder Facetten sowie bei der Geolokalisierungssuche und der
   Suche nach ähnlichen Dokumenten keine Ergebnisse; zurückgegeben werden dann nur die
   Ergebnisse der Schlüsselwortsuche. Einzelheiten zu den Bedingungen für das Überspringen
   finden Sie unter :doc:`search-semantic`.
3. Ergebnisse jedes Suchtyps einzeln überprüfen
4. Den Wert von ``rank.fusion.rank_constant`` anpassen
5. Bei tiefen Seiten (wo ``Startposition × 2`` größer oder gleich ``rank.fusion.window_size``
   ist, standardmäßig also ab dem 101. Ergebnis) wird keine Fusion durchgeführt und nur der
   Hauptsucher wird verwendet. Wenn Sie auf mehr Seiten fusionierte Ergebnisse wünschen, erhöhen
   Sie ``rank.fusion.window_size``.

Suche ist langsam
-----------------

**Symptom**: Suche wird bei aktiviertem Rank Fusion langsam

**Lösungen**:

1. ``rank.fusion.threads`` anpassen::

       rank.fusion.threads=4

2. ``rank.fusion.window_size`` reduzieren. Da der Wert die Untergrenze
   (``paging.search.page.max.size × 2``) nicht unterschreiten kann, setzen Sie in der
   Standardkonfiguration die folgenden beiden Werte gemeinsam::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   Beachten Sie, dass dadurch auch die maximale Anzahl an Ergebnissen sinkt, die pro Seite
   angefordert werden kann. Nach der Änderung ist ein Neustart erforderlich.

Speichermangel
--------------

**Symptom**: OutOfMemoryError tritt auf

**Lösungen**:

1. ``rank.fusion.window_size`` wie unter „Suche ist langsam" beschrieben reduzieren
2. JVM-Heap-Größe erhöhen

Referenz
========

- :doc:`search-semantic` - Konfiguration der semantischen Suche (Content-Chunking)
- :doc:`scripting-overview` - Scripting-Übersicht
- :doc:`search-advanced` - Erweiterte Sucheinstellungen
- :doc:`llm-overview` - LLM-Integrations-Leitfaden (Semantische Suche)
