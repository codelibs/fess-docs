====================================================
Semantische Suche (Content-Chunking + Vektorsuche)
====================================================

Übersicht
=========

In |Fess| 15.8 wurde die **Content-Chunking-Funktion** — die Dokumentinhalte in Chunks aufteilt
und für jeden Chunk einen Embedding-Vektor generiert und speichert — in den Kern integriert.
Die generierten Vektoren werden für zwei Zwecke verwendet:

- **Semantische Suche**: eine hybride Suche, die Schlüsselwortsuche (BM25) und Vektorsuche über
  Rank Fusion kombiniert. Dokumente, die der Anfrage semantisch nahestehen, können auch ohne
  exakte Schlüsselwortübereinstimmung gefunden werden.
- **KI-Suchmodus (RAG)**: Bei der Antwortgenerierung werden nur die Chunks, die der Frage
  semantisch am nächsten stehen, als Kontext für das LLM ausgewählt, was die Antwortqualität und
  die Token-Effizienz verbessert.

All dies ist standardmäßig deaktiviert. Solange Sie es nicht aktivieren, funktioniert |Fess|
weiterhin genau wie zuvor und verwendet ausschließlich die Schlüsselwortsuche. Wenn Sie |Fess| von
Version 15.7 oder früher aktualisieren oder das ``fess-webapp-semantic-search``-Plugin verwendet
haben, siehe :ref:`semantic-search-migration`.

Verarbeitungsablauf
--------------------

1. Der Crawler indiziert Dokumente wie gewohnt (zu diesem Zeitpunkt existieren noch keine Chunks).
2. Der Scheduler-Job **Content Chunk Vector Indexer** sucht nach unverarbeiteten Dokumenten,
   teilt deren Inhalt (das Feld ``content``) in Chunks auf, generiert Embedding-Vektoren und
   speichert sie im Feld ``content_chunk_vector``. Dabei wird auch das Feld ``content`` selbst
   in das Array der Chunks umgeschrieben (``content_length`` behält seinen ursprünglichen Wert).
3. Das Ergebnis dieser Verarbeitung wird im Feld ``content_chunk_status`` (unten beschrieben)
   festgehalten.
4. Wenn ``content_chunker.search.enabled=true`` gesetzt ist, nimmt der semantische Sucher zur
   Suchzeit an Rank Fusion teil.

Voraussetzungen
================

- **OpenSearch mit dem k-NN-Plugin**: In |Fess| 15.8 enthält das Mapping des Suchindex
  (``fess.search``) immer das Feld ``content_chunk_vector`` (ein ``nested``-Feld, dessen
  Unterfeld ``vector`` der ``knn_vector``-Typ für ANN ist), und die Indexeinstellungen enthalten
  immer ``index.knn: true`` — unabhängig davon, ob die Content-Chunking-Funktion aktiviert ist.
  Wenn OpenSearch das k-NN-Plugin nicht installiert hat, schlägt die Erstellung eines neuen Index
  daher grundsätzlich fehl, und |Fess| kann nicht starten.

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Konfiguration
       - Unterstützung des k-NN-Plugins
     * - Eingebettetes OpenSearch (``bin/fess`` oder die TAR.GZ/ZIP-Pakete, wenn
         ``SEARCH_ENGINE_HTTP_URL`` nicht gesetzt ist — der Standard)
       - Wird mit dem k-NN-Plugin ausgeliefert. Es enthält jedoch nicht die nativen
         JNI-Bibliotheken, sodass ``lucene`` die einzige unterstützte ANN-Engine ist.
         ``content_chunker.search.knn.engine`` akzeptiert auch ``faiss`` als Wert, und das
         Mapping wird auch dann erfolgreich erstellt — aber **bei jedem Schreibvorgang gehen
         Dokumente stillschweigend verloren, und Suchen liefern null Treffer**. (Wird |Fess| mit
         dieser Kombination gestartet, protokolliert es beim Start eine Warnung.)
     * - Docker (``ghcr.io/codelibs/fess-opensearch``), die RPM/DEB-Pakete (die sich immer mit
         einem separat installierten externen OpenSearch verbinden) oder ein weiteres externes
         OpenSearch (Standarddistribution)
       - Vollständig unterstützt, einschließlich ``faiss``.
     * - Die **Minimaldistribution** eines externen OpenSearch
       - **Nicht unterstützt.** Sie enthält das k-NN-Plugin nicht, sodass die Erstellung eines
         neuen Index fehlschlägt.

  ``nmslib`` ist bei keiner der obigen Konfigurationen ein zulässiger Wert für
  ``content_chunker.search.knn.engine``: ``content_chunk_vector`` ist ein ``nested``-Feld, und
  das k-NN-Plugin unterstützt nested Felder nur für die Engines ``lucene``/``faiss`` (``nmslib``
  ist außerdem ab OpenSearch 3.0 veraltet und eingeschränkt). Wird es dennoch gesetzt, greift mit
  einer Warnung der Fallback auf ``lucene``; die übrigen zulässigen Werte für die ANN-Einstellungen
  finden Sie unten in der Konfigurationsreferenz.

- **OpenSearch-Version eines externen Clusters**: Die mitgelieferten
  ``fess.search``-Indexeinstellungen senden in ``fess_indices/fess.json`` (sowie den
  AWS/Cloud-Varianten) immer ``index.knn`` und ``knn.derived_source.enabled``. Letzteres ist eine
  vergleichsweise neue Einstellung des k-NN-Plugins: Ein älteres OpenSearch, das sie nicht kennt,
  lässt die Erstellung des Index fehlschlagen — unabhängig davon, ob das k-NN-Plugin selbst
  installiert ist. Welche OpenSearch-Versionen |Fess| 15.8 unterstützt, entnehmen Sie
  :doc:`../install/prerequisites`.

- **Embedding-Anbieter**: Verwenden Sie einen der folgenden.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Konfigurationswert
     - Bereitgestellt durch
     - Beschreibung
   * - ``opensearch``
     - |Fess|-Kern (eingebaut)
     - Verwendet ein in OpenSearch ML Commons bereitgestelltes Embedding-Modell. Kein
       zusätzliches Plugin erforderlich. Standardeinstellung.
   * - ``ollama``
     - ``fess-llm-ollama``-Plugin
     - Verwendet ein Ollama-Embedding-Modell (z. B. ``nomic-embed-text``).
   * - ``openai``
     - ``fess-llm-openai``-Plugin
     - Verwendet die OpenAI-Embeddings-API.
   * - ``gemini``
     - ``fess-llm-gemini``-Plugin
     - Verwendet die Google-Gemini-Embeddings-API.
   * - ``none``
     - |Fess|-Kern (eingebaut)
     - Teilt Dokumente nur in Chunks auf; es werden keine Vektoren generiert (Nur-Chunk-Modus).

Konfigurationsreferenz
========================

Alle ``content_chunker.*``-Einstellungen liegen in einem einzigen Kanal: den
**Systemeigenschaften** (``system.properties``). Setzen Sie sie in
``app/WEB-INF/conf/system.properties`` (bei den RPM/DEB-Paketen ``/etc/fess/system.properties``,
unter Docker ``/opt/fess/system.properties``), oder geben Sie einen Initialwert über die
Startoption ``-Dfess.system.<key>`` an. Werte werden zur Laufzeit neu geladen, sodass die meisten
Einstellungen sofort nach der Änderung wirksam werden. Die einzige Ausnahme ist die Aktivierung
von ``content_chunker.search.enabled`` (``false`` → ``true``): Da der semantische Sucher nur beim
Start registriert wird, **erfordert diese Änderung einen Neustart, um wirksam zu werden**.

.. note::

   Die Liste der ``content_chunker.*``-Schlüssel ist auch in ``fess_config.properties`` als
   Kommentar aufgeführt, gelesen werden diese Schlüssel jedoch ausschließlich über den Kanal
   ``system.properties``. Einträge in ``fess_config.properties`` oder ``-Dfess.config.<key>``
   werden ignoriert — konfigurieren Sie sie daher stets in ``system.properties``. Der
   Admin-Bildschirm **Systeminformationen > Konfigurationsinformationen** zeigt lediglich die
   aktuellen Werte an und ist **rein lesend**; ``content_chunker.*`` lässt sich dort nicht setzen.

Einstellungen in system.properties
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Eigenschaft
     - Standard
     - Beschreibung
   * - ``content_chunker.enabled``
     - ``false``
     - Hauptschalter für die gesamte Content-Chunking-Funktion
   * - ``content_chunker.chunker.name``
     - ``length``
     - Chunking-Methode
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - Anzahl der Zeichen pro Chunk
   * - ``content_chunker.length.overlap``
     - ``0``
     - Anzahl der Zeichen, die sich zwischen Chunks überlappen
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - Maximale Anzahl von Chunks pro Dokument. Dokumente, die diesen Wert überschreiten, werden
       als ``skipped`` markiert
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - Embedding-Anbieter (``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``)
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - Dimension des Embedding-Vektors. Dieser Wert wird bei der Erstellung des Mappings
       verwendet und **muss** daher mit der Dimension des verwendeten Embedding-Modells
       übereinstimmen. Für diesen Wert gibt es zwei Lesepfade, die sich unterschiedlich verhalten.
       Bei der Erstellung des Index-Mappings wird mit einer Warnung ``768`` verwendet, wenn der
       Wert nicht gesetzt, nicht-numerisch, nicht positiv oder größer als ``16000`` (das Maximum
       des k-NN-Plugins selbst) ist. Zur Laufzeit des Embedding-Prozesses gibt es dagegen keinen
       Fallback: nicht gesetzte, nicht-numerische und nicht positive Werte führen jeweils zu einem
       Fehler. Werte über ``16000`` werden zur Laufzeit nicht abgelehnt, sodass nur das Mapping
       mit ``768`` erstellt wird und es zu einer Dimensionsabweichung kommt
   * - ``content_chunker.job.concurrency``
     - ``2``
     - Anzahl paralleler Worker für den Indexer-Job
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - Anzahl der pro Batch abgerufenen und geschriebenen Dokumente
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ (unbegrenzt)
     - Maximale Anzahl der pro Job-Lauf verarbeiteten Dokumente. Jeder Wert von ``0`` oder
       kleiner wird als unbegrenzt behandelt
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - Wenn auf ``true`` gesetzt, werden Dokumente, deren vorheriger Lauf mit
       ``content_chunk_status=fail`` endete, auch in das Verarbeitungsziel des nächsten Laufs
       einbezogen. Es gibt keine automatische Wiederholung oder Zählung der Versuche; der
       vorgesehene Arbeitsablauf besteht darin, die zugrunde liegende Ursache zu beheben und
       dies dann vorübergehend zu aktivieren, um es erneut zu versuchen
   * - ``content_chunker.chat.top_k``
     - ``3``
     - Anzahl der Chunks, die bei der Antwortgenerierung im KI-Suchmodus ausgewählt werden
   * - ``content_chunker.search.enabled``
     - ``false``
     - Rank-Fusion-Integration für die semantische Suche (**die Aktivierung erfordert einen
       Neustart**)
   * - ``content_chunker.search.min_score``
     - (nicht gesetzt)
     - Minimale Kosinusähnlichkeit (0–1), die für die Aufnahme eines Ergebnisses erforderlich
       ist. Ohne diesen Wert erfolgt kein Cutoff. Im Modus ``ann`` wird der Cutoff mit einer
       Warnung übersprungen, wenn ``search.knn.space_type`` nicht ``cosinesimil`` ist, da sich
       dann kein kosinusbasierter Cutoff definieren lässt
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANN-Indexmethode. ``hnsw`` ist derzeit der einzige zulässige Wert; jeder andere Wert führt
       mit einer Warnung zum Fallback auf ``hnsw`` (wird im Mapping abgebildet; eine Änderung
       erfordert die Neuerstellung des Index)
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANN-Engine. Zulässig sind nur ``lucene`` oder ``faiss`` (siehe Voraussetzungen oben); jeder
       andere Wert führt mit einer Warnung zum Fallback auf ``lucene`` (wird im Mapping
       abgebildet; eine Änderung erfordert die Neuerstellung des Index)
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - Distanzraum. Zulässig sind nur ``cosinesimil``, ``innerproduct`` oder ``l2``; jeder andere
       Wert führt mit einer Warnung zum Fallback auf ``cosinesimil`` (wird im Mapping abgebildet;
       eine Änderung erfordert die Neuerstellung des Index)
   * - ``content_chunker.search.knn.k``
     - ``100``
     - Anzahl der pro ANN-Abfrage abgerufenen Nachbarn (wird für Deep Paging automatisch
       vergrößert)
   * - ``content_chunker.search.knn.param.ef_search``
     - (nicht gesetzt)
     - Der Parameter ``ef_search`` für ANN-Abfragen

.. note::

   Die HNSW-Parameter ``m`` und ``ef_construction`` sind in ``doc.json`` fest codiert
   (``m=16`` / ``ef_construction=100``) und können nicht über die Konfiguration geändert werden.

Verbindungseinstellungen für den Anbieter opensearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verbindungseinstellungen für den eingebauten Anbieter ``opensearch`` (OpenSearch ML Commons).
Diese werden in derselben Datei ``system.properties`` wie oben gesetzt.

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - Eigenschaft
     - Standard
     - Beschreibung
   * - ``content_chunker.embedding.opensearch.model.id``
     - (erforderlich)
     - ID des bereits in ML Commons bereitgestellten Modells
   * - ``content_chunker.embedding.opensearch.api.url``
     - Adresse der Suchmaschine
     - ML-Commons-API-Endpunkt. Ohne diese Einstellung wird standardmäßig die Suchmaschine
       verwendet, die |Fess| bereits nutzt (z. B. ``http://localhost:9200``)
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - Zugangsdaten der Suchmaschine
     - Ohne diese Einstellung werden die für die Verbindung zur Suchmaschine verwendeten
       Zugangsdaten übernommen — jedoch nur, solange ``api.url`` nicht konfiguriert ist (d. h.
       das Ziel ist dasselbe Cluster, das |Fess| bereits verwendet). Sobald ``api.url`` gesetzt
       ist, entfällt dieser Fallback.
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - Anfrage-Timeout (ms)
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - Verbindungs-Timeout (ms)
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - Anzahl der Wiederholungen bei vorübergehenden Fehlern (429, 5xx usw.)
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - Basisverzögerung für Wiederholungen (ms)
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - Intervall zwischen Verfügbarkeitsprüfungen des Anbieters (Sekunden)
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - (leer)
     - Präfix, das dem Dokument-/Anfragetext vor dem Embedding vorangestellt wird

.. warning::

   Der Inhalt von ``system.properties`` ist im Admin-Bildschirm **Systeminformationen >
   Konfigurationsinformationen**, im Bereich **App-Eigenschaften**, einsehbar.
   ``content_chunker.embedding.opensearch.password`` wird auf diesem Bildschirm zu ``XXXXXXXX``
   maskiert, ``username`` dagegen unverändert angezeigt. Werte, die Sie über
   ``-Dfess.system.<key>`` angeben, erscheinen auf demselben Bildschirm im Bereich
   **Systemeigenschaften** **unmaskiert** — tragen Sie Zugangsdaten daher in
   ``system.properties`` ein und nicht in die Startoptionen.

Andere Anbieter (ollama / openai / gemini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Anbieter ``ollama`` (``fess-llm-ollama``-Plugin) verwendet denselben Einstellungsstil unter
dem Präfix ``content_chunker.embedding.ollama.`` (``api.url`` ist standardmäßig
``http://localhost:11434``, ``model`` standardmäßig ``embeddinggemma``, und
``document.prefix`` / ``query.prefix`` sind standardmäßig ``title: none | text:`` bzw.
``task: search result | query:``). Verwenden Sie ein Modell der ``nomic-embed-text``-Familie,
setzen Sie ``document.prefix`` / ``query.prefix`` explizit auf ``search_document:`` bzw.
``search_query:``. Diese Präfixe werden unverändert mit dem einzubettenden Text verkettet
(umgebende Leerzeichen werden nicht entfernt), daher enthalten sowohl die obigen Standardwerte
als auch ``search_document:`` bzw. ``search_query:`` jeweils **ein abschließendes Leerzeichen**.
Denken Sie an das trennende Leerzeichen, wenn Sie ein Präfix selbst setzen.
Die Anbieter ``openai`` und ``gemini`` werden auf dieselbe Weise
konfiguriert, unter den Präfixen ``content_chunker.embedding.openai.`` bzw.
``content_chunker.embedding.gemini.``. Die vollständige Liste der Einstellungen finden Sie in der
jeweiligen Plugin-Dokumentation.

Einrichtungsverfahren (Beispiel mit dem Anbieter opensearch)
================================================================

Dieser Abschnitt führt durch ein Konfigurationsbeispiel mit dem eingebauten Anbieter
``opensearch`` (ML Commons).

1. Embedding-Modell bereitstellen
------------------------------------

Registrieren und bereitstellen Sie ein Embedding-Modell in OpenSearch ML Commons. In einem
Single-Node-Cluster müssen Sie zunächst die folgende Einstellung anwenden.

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

Registrieren und bereitstellen Sie das Modell (Beispiel: ein Sentence-Embedding-Modell mit
384 Dimensionen):

.. code-block:: bash

    # Modell registrieren (model_id aus dem task_id der Antwort entnehmen)
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # Abschluss der Aufgabe prüfen und model_id abrufen
    # (sobald state auf COMPLETED steht, wird model_id zurückgegeben)
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # Bereitstellen
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # Status prüfen: model_state sollte DEPLOYED sein
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   Ein Modell, das sich noch im Status ``REGISTERED`` befindet, kann nicht verwendet werden.
   Stellen Sie sicher, dass Sie es bereitstellen und bestätigen, dass ``model_state`` zu
   ``DEPLOYED`` wird.

2. |Fess| konfigurieren
--------------------------

``app/WEB-INF/conf/system.properties`` (bei den RPM/DEB-Paketen ``/etc/fess/system.properties``,
unter Docker ``/opt/fess/system.properties``; alles Folgende gehört in dieselbe Datei)::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

Wenn Sie zusätzlich die semantische Suche nutzen möchten, fügen Sie außerdem Folgendes hinzu::

    content_chunker.search.enabled=true

Starten Sie |Fess| nach diesen Änderungen neu.

3. Index neu erstellen (bei Aktivierung auf einer bestehenden Installation)
-------------------------------------------------------------------------------

Das Mapping für das Feld ``content_chunk_vector`` — einschließlich der von Ihnen konfigurierten
Dimension und ANN-Methodeneinstellungen — wird **in dem Moment angewendet, in dem der Index**
``fess.search`` **neu erstellt wird**.

- **Neuinstallationen**: Wenn Sie die obigen Einstellungen in ``system.properties`` anwenden,
  bevor Sie |Fess| zum ersten Mal starten, wird das korrekte Mapping automatisch angewendet, wenn
  der Index erstmals erstellt wird; dieser Schritt ist dann nicht erforderlich.
- **Wenn bereits ein Index existiert** (das heißt, wenn Sie |Fess| bereits mindestens einmal
  gestartet haben): Der laufende Index übernimmt das neue Mapping nicht automatisch, und ein
  bestehendes Mapping kann nachträglich nicht geändert werden. Erstellen Sie den Index wie folgt
  neu:

  Öffnen Sie **Systeminformationen > Wartung**, und führen Sie unter **Neuindizierung** die
  Neuindizierung mit aktivierter Option **Aliase ersetzen** aus.

  Anschließend können Sie bestätigen, dass der neu erstellte Index ``index.knn: true`` in den
  Indexeinstellungen sowie ein ``content_chunk_vector``-Mapping mit der von Ihnen konfigurierten
  Dimension und den ANN-Methodeneinstellungen enthält (``index.knn`` gehört zu den
  Indexeinstellungen, die ANN-Methodeneinstellungen zum Mapping — zwei verschiedene Ziele).

.. warning::

   Die Neuindizierung läuft als asynchroner Hintergrundprozess, und die Admin-Oberfläche zeigt
   keine Erfolgsmeldung an. ``_cat/indices`` zeigt nur, dass der neue Index existiert (Status,
   Dokumentanzahl usw.) — nicht, worauf die Aliase zeigen. Bevor Sie mit dem unten beschriebenen
   Indexer-Job fortfahren, prüfen Sie stattdessen ``_cat/aliases`` und vergewissern Sie sich, dass
   sowohl ``fess.search`` als auch ``fess.update`` auf den neuen Index zeigen; das |Fess|-Log
   protokolliert nur bei einem Fehler eine Warnung, sodass ein stilles Log kein Erfolgsnachweis
   ist, sondern nur das Fehlen eines bekannten Fehlers anzeigt. Der alte Index (der physische
   Index, auf den der Alias ``fess.search`` zuvor verwies, benannt ``fess.<timestamp>``) wird
   nicht automatisch gelöscht; entfernen Sie ihn manuell, sobald Sie ihn nicht mehr benötigen.
   Solange beide Indizes existieren, ist mit etwa der doppelten üblichen Index-Festplattennutzung
   zu rechnen.

4. Indexer-Job aktivieren
-----------------------------

Chunking und Embedding-Generierung werden vom Scheduler-Job **Content Chunk Vector Indexer**
durchgeführt (ID: ``content-chunk-vector-indexer``; standardmäßig deaktiviert; geplant mit
``0 13 * * *``).

Aktivieren Sie diesen Job unter **System > Scheduler** und führen Sie ihn dann einmal mit
**Jetzt starten** aus. Danach werden unverarbeitete Dokumente unabhängig vom Abschluss eines
Crawls gemäß dem konfigurierten Zeitplan (standardmäßig täglich um 13:00 Uhr) verarbeitet. Der
Job ist nicht mit dem Crawl-Job verkettet; wenn Sie unmittelbar nach einem Crawl verarbeiten
möchten, legen Sie den Zeitplan auf einen Zeitpunkt nach dem erwarteten Ende des Crawl-Jobs.

.. note::

   In einer Multi-Node-Bereitstellung empfehlen wir, diesen Job an genau einen Knoten zu binden.
   Wird er auf jedem Knoten gleichzeitig ausgeführt, führt dies zwar nicht zu Fehlern in der
   Korrektheit, aber jeder Knoten verarbeitet und embeddet dieselben Dokumente redundant, was die
   Last und die Kosten bei Ihrem Embedding-Anbieter um die Anzahl der Knoten vervielfacht.

   Die Bindung erfordert **beide** der folgenden Einstellungen — jede für sich allein bindet den
   Job nicht.

   1. **Auf dem Knoten, auf dem der Job laufen soll**: Setzen Sie
      ``scheduler.target.name=<eine Kennung>`` in
      ``app/WEB-INF/classes/fess_config.properties`` (bei den RPM/DEB-Paketen
      ``/etc/fess/fess_config.properties``; oder über
      ``-Dfess.config.scheduler.target.name=<eine Kennung>``) und starten Sie diesen Knoten neu.
      (Der Standardwert ist leer; belassen Sie alle anderen Knoten auf dem Standardwert.)
   2. Öffnen Sie in der Admin-Oberfläche unter **System > Scheduler** den Job Content Chunk
      Vector Indexer und ändern Sie dessen Feld **Ziel** von ``all`` auf dieselbe Kennung, die
      Sie in Schritt 1 gesetzt haben, und speichern Sie.

   Was das Feld **Ziel** bedeutet, entnehmen Sie :doc:`../admin/scheduler-guide`. Das alleinige
   Setzen von ``scheduler.target.name`` bindet den Job nicht, wenn das Feld **Ziel** auf ``all``
   belassen wird: **er wird dann nicht gebunden**. ``all`` wird als Sonderwert behandelt, der
   immer zutrifft, sodass Schritt 1 allein oder Schritt 2 allein nicht ausreicht — Sie müssen
   beides tun.

.. warning::

   Führen Sie **Jetzt starten** nach der Bindung ebenfalls **über die Admin-Oberfläche des
   Knotens aus, für den Sie in Schritt 1 die Kennung gesetzt haben**. Drücken Sie **Jetzt
   starten** auf einem anderen Knoten, meldet der Bildschirm zwar „Job … gestartet.", der Job
   läuft aber wegen der Abweichung im Feld **Ziel** nicht (im Log dieses Knotens erscheint
   lediglich eine INFO-Zeile ``Ignoring job``).

5. Verarbeitungsstatus prüfen
---------------------------------

Sie können das Ergebnis für jedes Dokument in dessen Feld ``content_chunk_status`` prüfen.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Wert
     - Bedeutung
   * - (Feld fehlt)
     - Noch nicht verarbeitet (wird beim nächsten Job-Lauf aufgenommen). Dokumente kehren nach
       einem erneuten Crawl ebenfalls in diesen Zustand zurück
   * - ``done``
     - Chunking und Vektorgenerierung abgeschlossen
   * - ``chunked``
     - Nur Chunking abgeschlossen (Nur-Chunk-Modus). Das gilt für ``embedding.name=none``, aber
       ebenso, wenn das Plugin des unter ``embedding.name`` angegebenen Anbieters nicht
       installiert ist
   * - ``skipped``
     - Verarbeitung übersprungen (z. B. ``max_chunks_per_document`` überschritten)
   * - ``fail``
     - Verarbeitung fehlgeschlagen (Protokolle prüfen)

Sie können die Verteilung der Statuswerte durch eine direkte Abfrage der Suchmaschine prüfen::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

Durch die Option ``missing`` werden Dokumente ohne ``content_chunk_status`` (also unverarbeitete
Dokumente) in einem Bucket mit dem Schlüssel ``pending`` zusammengefasst.

Verhalten der semantischen Suche
====================================

Das Setzen von ``content_chunker.search.enabled=true`` registriert den semantischen Sucher bei
Rank Fusion, das dann die Ergebnisse der Schlüsselwortsuche mit denen der Vektorsuche
zusammenführt. (Siehe :doc:`rank-fusion` für die Funktionsweise von Rank Fusion.)
Zur Suchzeit wird zusätzlich ``content_chunker.enabled`` ausgewertet: Bei
``content_chunker.enabled=false`` oder ``content_chunker.embedding.name=none`` findet keine
semantische Suche statt, auch wenn der Sucher registriert ist (diese Prüfung erfolgt pro Anfrage,
ein Neustart ist also nicht nötig).

.. warning::

   Da der semantische Sucher beim Start registriert wird, **erfordert die Aktivierung einen
   Neustart**. Das Deaktivieren (Zurücksetzen des Werts auf ``false``) wird pro Anfrage
   ausgewertet und wirkt daher sofort.

Modus exact und Modus ann
-----------------------------

Die Suchmethode wird automatisch anhand des Zustands des Index gewählt.

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - Modus
     - Bedingung
     - Merkmale
   * - ``ann``
     - Ein Index mit ``index.knn``- und ANN-Methodeneinstellungen
     - Approximate-Nearest-Neighbor-Suche mit HNSW. Geeignet für große Indizes
   * - ``exact``
     - Alles andere (ein Index, dem entweder ``index.knn`` oder die ANN-Methodeneinstellungen
       fehlen — einschließlich des Falls, dass die Ermittlung des Indexzustands fehlschlägt)
     - Exakte Kosinusähnlichkeitsberechnung über jeden Vektor. Geeignet für kleine bis mittlere
       Indizes

Jeder unter |Fess| 15.8 neu erstellte ``fess.search``-Index hat immer ``index.knn``- und
ANN-Methodeneinstellungen, unabhängig vom Wert von ``content_chunker.search.enabled`` — daher
wird normalerweise stets der Modus ``ann`` verwendet. Der Modus ``exact`` ist ein Fallback für
ältere Indizes, die vor der Einführung dieses Mechanismus erstellt wurden. Da k-NN-Einstellungen
einem bestehenden Index nicht nachträglich hinzugefügt werden können, erfordert der Wechsel eines
Index im Modus ``exact`` in den Modus ``ann`` die Neuerstellung des Index (siehe
:ref:`semantic-search-migration`). Das Ergebnis dieser Ermittlung wird 60 Sekunden lang
zwischengespeichert; unmittelbar nach einer Neuerstellung des Index kann es daher bis zu
60 Sekunden dauern, bis die Umstellung wirksam wird.

Score-Cutoff
--------------

Das Setzen von ``content_chunker.search.min_score`` auf eine Kosinusähnlichkeit (0–1) schließt
Dokumente von den Ergebnissen der semantischen Suche aus, deren bester Chunk diesen Wert nicht
erreicht (da der Score eines Dokuments der Score seines besten Chunks ist, wirkt der Cutoff auf
Dokumentebene). Verwenden Sie dies, um die Trefferzahl bei Anfragen ohne Vokabularüberschneidung
einzugrenzen, wenn diese zu breit gestreut werden::

    content_chunker.search.min_score=0.4

Der konfigurierte Wert wird sowohl im Modus ``exact`` als auch im Modus ``ann`` als
Kosinusähnlichkeit interpretiert (intern wird er in die Score-Skala des jeweiligen Modus
umgerechnet).

.. note::

   Dieser Cutoff wird nur angewendet, wenn ``content_chunker.search.knn.space_type`` auf
   ``cosinesimil`` (dem Standard) steht. Bei einem Index im Modus ``ann`` mit ``innerproduct``
   oder ``l2`` lässt sich keine Kosinusähnlichkeit definieren; der Cutoff wird dann übersprungen,
   nachdem einmalig eine Warnung protokolliert wurde.

Einschränkungen
------------------

- **Die semantische Suche wird bei Anfragen mit Suchsyntax übersprungen**, und es läuft nur die
  Schlüsselwortsuche. Die Prüfung erfolgt an der **fertig zusammengesetzten** Anfragezeichenkette
  und greift, sobald diese eines der Zeichen ``"`` ``(`` ``)`` ``:`` ``[`` ``]`` ``{`` ``}``
  ``^`` ``~`` ``*`` ``?`` ``\``, die Folgen ``&&`` oder ``||``, ein ``+`` bzw. ``-`` am Anfang
  oder direkt nach einem Leerzeichen oder eines der Großbuchstabenwörter ``AND`` / ``OR`` /
  ``NOT`` / ``TO`` enthält. Auch ohne dass Nutzende selbst Suchsyntax eingeben, wird die
  semantische Suche daher bei den folgenden Vorgängen übersprungen.

  - Auswahl eines Labels (intern wird ``label:"..."`` angehängt)
  - Angabe einer Sortierbedingung (intern wird ``sort:...`` angehängt)
  - Eingrenzung über Facetten (intern wird z. B. ``filetype:...`` angehängt)
  - Phrasensuche, Ausschlusswörter, Dateityp, Site und Zeitraum in der erweiterten Suche
  - Suchbegriffe mit hinterlegten verwandten Anfragen (intern zu ``("A" OR "B")`` expandiert)

  Da auch das ASCII-Zeichen ``?`` dazugehört, wird ein natürlichsprachlicher Satz, der mit einem
  ASCII-Fragezeichen endet (etwa „Was ist ...?"), übersprungen (das Vollbreiten-``？`` zählt
  nicht dazu).
- Sie wird ebenfalls übersprungen, wenn sie mit der Geolokalisierungssuche (einem Geo-Filter)
  oder der Suche nach ähnlichen Dokumenten kombiniert wird.
- Auf tiefen Ergebnisseiten wird Rank Fusion selbst deaktiviert, sodass nur Ergebnisse der
  Schlüsselwortsuche zurückgegeben werden. Die Grenze bestimmt
  ``rank.fusion.window_size`` (Standard ``200``); damit betrifft dies standardmäßig alle Treffer
  ab dem 101. Suchergebnis.
- Ist der Embedding-Anbieter nicht erreichbar oder tritt ein Suchfehler auf, fällt |Fess|
  automatisch auf reine Schlüsselwortergebnisse zurück (die Suche selbst schlägt dadurch nie
  fehl).
- Die rollen- und virtual-host-basierte Zugriffskontrolle gilt auch für Ergebnisse der
  semantischen Suche.

Integration mit dem KI-Suchmodus
====================================

Wenn der KI-Suchmodus (:doc:`rag-chat`, ``rag.chat.enabled=true``) aktiviert ist, berechnet die
Antwortgenerierung für Dokumente, deren ``content_chunk_status`` ``done`` ist, die Ähnlichkeit
zu jedem Chunk und verwendet nur die ``content_chunker.chat.top_k`` relevantesten Chunks
(Standard: ``3``) als Kontext für das LLM.

Eingebettet wird dabei nicht die Äußerung der Nutzenden selbst, sondern die **vom LLM in der
Phase der Absichtserkennung generierte Suchanfrage** (bei einer erneuten Suche entsprechend die
neu generierte Anfrage). Wird keine Suchanfrage generiert — etwa wenn um die Zusammenfassung
eines Dokuments gebeten wird —, findet keine Chunk-Auswahl statt.

Dadurch werden selbst bei langen Dokumenten nur die relevanten Abschnitte an das LLM übergeben,
was die Antwortgenauigkeit verbessern und die Token-Nutzung reduzieren kann. Bei Dokumenten mit
``content_chunk_status`` ``chunked`` (Chunks vorhanden, aber keine Vektoren) erfolgt die
Chunk-Auswahl statt über die Ähnlichkeitsberechnung über Schlüsselwort- bzw.
Hervorhebungstreffer. Dokumente mit ``skipped`` oder ``fail`` sowie unverarbeitete Dokumente
verwenden wie bisher den vollständigen Inhalt (oder einen hervorgehobenen Ausschnitt).

Dieses Verhalten ist unabhängig von ``content_chunker.search.enabled``, setzt aber voraus, dass
``content_chunker.enabled`` aktiviert ist. Beachten Sie außerdem, dass auch der aus den
ausgewählten Chunks zusammengesetzte Text auf ``rag.chat.content.fulltext.max.length``
(Standard ``3000``) gekürzt wird: Selbst wenn Sie ``content_chunker.chat.top_k`` oder
``content_chunker.length.chunk_size`` erhöhen, überschreitet die an das LLM übergebene
Zeichenzahl diese Obergrenze nicht.

.. _semantic-search-migration:

Migration von 15.7 oder früheren Versionen
=============================================

Wenn Sie |Fess| von Version 15.7 oder früher aktualisieren, fällt Ihre Situation je nachdem, wie
Sie diese Funktionen aktuell nutzen, in eines der vier folgenden Muster. Folgen Sie den
Anweisungen für das für Sie zutreffende Muster.

Neuinstallationen
--------------------

Es ist keine zusätzliche Arbeit erforderlich. Wenn Sie die Vektorsuche nutzen möchten,
konfigurieren Sie ``system.properties`` einfach gemäß dem Abschnitt *Konfigurationsreferenz* auf
dieser Seite, bevor Sie |Fess| zum ersten Mal starten; das korrekte Mapping wird automatisch
angewendet, wenn der Index erstmals erstellt wird. (Die konkreten Schritte finden Sie oben unter
*Einrichtungsverfahren*.)

.. note::

   Wenn Sie |Fess| bereits mindestens einmal gestartet haben (das heißt, der Index bereits
   existiert), folgen Sie stattdessen einem der unten stehenden Muster für *bestehende Nutzer*.

Bestehende Nutzer, die keine Vektorsuche wünschen
------------------------------------------------------

Es ist keine Arbeit erforderlich. ``content_chunker.enabled`` und
``content_chunker.search.enabled`` sind beide standardmäßig ``false``, sodass sich Ihre
Suchergebnisse und das bestehende Indexverhalten nach dem Upgrade nicht ändern. Der neue
Scheduler-Job **Content Chunk Vector Indexer** wird beim Start automatisch registriert, läuft
aber, da er standardmäßig deaktiviert ist, nie, und der semantische Sucher wird nie bei Rank
Fusion registriert. (Der Job wird bei jedem Start registriert; löschen Sie ihn in der
Admin-Oberfläche, wird er beim nächsten Start im deaktivierten Zustand neu angelegt.)

.. note::

   Auch wenn Sie die Vektorsuche nicht nutzen: Sobald ab |Fess| 15.8 ein Index **neu erstellt**
   wird (einschließlich einer Neuindizierung), werden das Mapping mit ``content_chunk_vector``
   (Typ ``knn_vector``) und ``index.knn: true`` angewendet. In einer Konfiguration ohne das
   k-NN-Plugin in OpenSearch schlägt die Erstellung des Index dann genau an dieser Stelle fehl.
   Einzelheiten finden Sie im Abschnitt *Voraussetzungen* auf dieser Seite.

Bestehende Nutzer, die die Vektorsuche aktivieren möchten
----------------------------------------------------------

Der laufende Index übernimmt das neue Mapping nicht automatisch, daher sind die folgenden
Schritte erforderlich.

1. Wenden Sie die Einstellungen wie im Abschnitt *Konfigurationsreferenz* auf dieser Seite
   beschrieben auf ``system.properties`` an (die konkreten Schritte bei Verwendung des Anbieters
   opensearch finden Sie oben unter *Einrichtungsverfahren*).
2. Starten Sie |Fess| neu.
3. Führen Sie in der Admin-Oberfläche unter **Systeminformationen > Wartung** die
   **Neuindizierung** mit aktivierter Option **Aliase ersetzen** aus. Dies läuft im Hintergrund
   ohne Erfolgsmeldung ab. ``_cat/indices`` zeigt nur, dass der neue Index existiert, nicht ob die
   Aliase umgeschaltet wurden — prüfen Sie stattdessen ``_cat/aliases`` und vergewissern Sie sich,
   dass ``fess.search``/``fess.update`` auf den neuen Index zeigen (das |Fess|-Log warnt nur bei
   einem Fehler, Stille ist also kein Erfolgsnachweis). Der alte Index wird nicht automatisch
   gelöscht (entfernen Sie ihn manuell, sobald Sie ihn nicht mehr benötigen); bis dahin verdoppelt
   sich in etwa die Index-Festplattennutzung.
4. Erst nachdem Sie den oben genannten Alias-Wechsel bestätigt haben, aktivieren und starten Sie
   den Job Content Chunk Vector Indexer unter **System > Scheduler** (ein erneutes Crawlen ist
   nicht erforderlich: Der Job liest ``content`` aus der ``_source`` des bestehenden Index, um es
   zu chunken und zu embedden).

.. note::

   Wenn Sie bereits in Schritt 1 ``content_chunker.search.enabled=true`` setzen, wird zwischen
   dem Neustart in Schritt 2 und dem Abschluss von Schritt 4 bei jeder Suche lediglich die
   Anfrage eingebettet, ohne dass sich dies in den Ergebnissen niederschlägt. Bei
   nutzungsabhängig abgerechneten Anbietern wie ``openai`` oder ``gemini`` sollten Sie
   ``content_chunker.search.enabled=true`` daher erst nach Abschluss von Schritt 4 setzen und
   |Fess| dann neu starten.

Wenn Sie das Plugin fess-webapp-semantic-search verwendet haben
------------------------------------------------------------------

Das Plugin ``fess-webapp-semantic-search``, das die semantische Suche in |Fess| 15.7 und früher
bereitstellte, wurde in 15.8 in den Kern integriert und ist nun **unnötig (veraltet)**.
Zusätzlich zu den oben unter *Bestehende Nutzer, die die Vektorsuche aktivieren möchten*
beschriebenen Schritten müssen Sie außerdem Folgendes tun.

1. **Plugin entfernen**: Löschen Sie ``fess-webapp-semantic-search-*.jar`` aus
   ``app/WEB-INF/plugin/`` (schließen Sie es unter Docker aus ``FESS_PLUGINS`` aus).

2. **Alte Einstellungen entfernen**: Löschen Sie jede Startoption ``-Dfess.semantic_search.*``.
   Wenn Sie außerdem ``-Drank.fusion.searchers=default,semantic`` für das alte Plugin angegeben
   hatten, entfernen Sie dies ebenfalls. Wird es beibehalten, schließt es den neuen semantischen
   Sucher (``semantic_chunk``) von Rank Fusion aus und protokolliert beim Start eine Warnung.

3. **Alte Ingest-Pipeline lösen**: Sofern ``-Dfess.semantic_search.pipeline`` konfiguriert war,
   trägt das alte Plugin bei der Erstellung des Index ``default_pipeline`` (eine Ingest-Pipeline
   für die neuronale Suche) in die Indexeinstellungen ein. **Das Entfernen des Plugins entfernt
   die Pipeline nicht** — sie bleibt am Index angehängt und läuft weiter —, sodass Sie sie lösen
   müssen, und zwar **vor** der Neuindizierung aus dem Abschnitt *Bestehende Nutzer, die die
   Vektorsuche aktivieren möchten*. Der nach der Neuindizierung erstellte neue Index trägt diese
   Einstellung nicht mehr, ein späteres Ausführen des Befehls bliebe also wirkungslos. Ermitteln
   Sie mit ``_cat/aliases``, auf welches ``fess.<timestamp>`` der Alias ``fess.search`` zeigt,
   und geben Sie den konkreten Indexnamen an, nicht den Alias::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   Das Lösen der Indexeinstellung entfernt die Ingest-Pipeline selbst nicht aus der Suchmaschine.
   Löschen Sie sie separat, wenn Sie sie künftig nicht mehr benötigen::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<pipeline-name>"

4. **Neue Einstellungen hinzufügen**: Konfigurieren Sie ``content_chunker.*`` in
   ``system.properties`` wie im Abschnitt *Konfigurationsreferenz* auf dieser Seite beschrieben.
   Wenn Sie Ihr bestehendes ML-Commons-Modell weiter verwenden, setzen Sie
   ``content_chunker.embedding.name=opensearch`` und tragen Sie dessen bestehende ``model_id``
   in ``content_chunker.embedding.opensearch.model.id`` ein.

5. **Index neu erstellen und Job ausführen**: Das Vektorfeld, das das alte Plugin speicherte
   (in der Standardkonfiguration ``content_vector``), und das Feld ``content_chunk_vector``, das
   die neue Kernfunktion verwendet, sind unterschiedliche Felder; die alten Vektoren lassen sich
   mit der neuen Funktion nicht nutzen. Die Neuindizierung kopiert ``_source`` jedoch unverändert,
   sodass die alten Vektoren auch in den neuen Index übernommen werden und dort über das
   dynamische Mapping dauerhaft Festplattenspeicher verbrauchen. Wir empfehlen daher, sie **vor**
   der Neuindizierung zu entfernen (falls Sie den Feldnamen geändert haben, passen Sie ihn
   entsprechend an)::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   Führen Sie anschließend die **Neuindizierung** unter **Systeminformationen > Wartung** aus und
   aktivieren und starten Sie danach den Job Content Chunk Vector Indexer, um die Vektoren neu zu
   generieren.

Hinweise
==========

Das Embedding-Modell (Dimension) wechseln
--------------------------------------------

Um zu einem Embedding-Modell mit einer anderen Dimension zu wechseln, gehen Sie in dieser
Reihenfolge vor.

1. Löschen Sie die bestehenden, alten Vektoren. Bleiben Vektoren in der alten Dimension bei der
   Neuindizierung erhalten, akzeptiert das neue Mapping sie nicht, und die Verarbeitung läuft
   weiter, ohne die betroffenen Dokumente in den neuen Index zu kopieren. Da |Fess| nur den
   HTTP-Status der Neuindizierung prüft, zeigt die Admin-Oberfläche keinen Fehler an, während
   Dokumente verloren gehen::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      Als Ziel können Sie ebenso gut ``fess.update`` (den Update-Alias, aus dem die
      Neuindizierung liest) angeben. Beachten Sie außerdem, dass das Feld ``content`` bei diesem
      Vorgang ein Array von Chunks bleibt. Beim nächsten Job-Lauf wird es wieder zusammengefügt
      und neu aufgeteilt; ist ``content_chunker.length.overlap`` auf einen Wert ungleich 0
      gesetzt, sind die Überlappungen dabei doppelt enthalten. Wenn Sie das vermeiden möchten,
      crawlen Sie die betroffenen Dokumente erneut.

2. Ändern Sie ``content_chunker.embedding.dimension`` und die Modelleinstellung für Ihren
   Anbieter.
3. Erstellen Sie den Index gemäß dem Abschnitt *3. Index neu erstellen (bei Aktivierung auf einer
   bestehenden Installation)* unter *Einrichtungsverfahren* neu und führen Sie den Indexer-Job
   erneut aus.

Festplattennutzung
---------------------

Chunk-Vektoren werden zusätzlich zu den Suchindexstrukturen in ``_source`` vorgehalten, sodass
jedes Dokument zusätzlichen Festplattenspeicher proportional zur Anzahl seiner Chunks
multipliziert mit der Vektordimension verbraucht. Wenn der Festplattenspeicher knapp wird, passen
Sie ``content_chunker.length.chunk_size`` oder ``content_chunker.max_chunks_per_document`` an.

Nur-Chunk-Modus
------------------

Das Setzen von ``content_chunker.embedding.name=none`` führt nur das Chunking durch, ohne
Embedding-Vektoren zu generieren (``content_chunk_status`` wird zu ``chunked``). Damit können Sie
das Chunking bereits durchführen, bevor Ihr Embedding-Anbieter bereit ist; sobald Sie später
einen Anbieter konfigurieren und den Job erneut ausführen, werden für die bereits gespeicherten
Chunks Vektoren generiert, ohne dass diese erneut gechunkt werden.

Speichereinstellungen für große Korpora
-------------------------------------------

Die Kind-JVM des Indexer-Jobs wird mit ``jvm.chunk.options`` in ``fess_config.properties``
gestartet (JVM-Optionen, die standardmäßig ``-Xms128m -Xmx1g`` enthalten). Da
``content_chunker.job.max_documents_per_run`` standardmäßig unbegrenzt ist, hält ein einzelner
Lauf alle ausstehenden Dokument-IDs im Speicher. Eine Dokument-ID ist ein SHA-512-Digest
(128 Zeichen) und belegt im Heap rund 200 Byte; die Chunk-Verarbeitung selbst benötigt zusätzlich
etwa 200–250 MB. Erhöhen Sie daher bei **Korpora ab etwa 1 bis 2 Millionen Dokumenten** den
``-Xmx``-Wert in ``jvm.chunk.options`` oder setzen Sie
``content_chunker.job.max_documents_per_run`` auf einen endlichen Wert, um die Verarbeitung auf
mehrere Läufe aufzuteilen. ``jvm.chunk.options`` überschreiben Sie in
``app/WEB-INF/classes/fess_config.properties`` (bei den RPM/DEB-Paketen
``/etc/fess/fess_config.properties``); siehe :doc:`setup-memory` zum Umgang mit JVM-Optionen.

Derselbe unbegrenzte Standardwert hat auch Kostenfolgen bei einem nutzungsabhängig abgerechneten
Embedding-Anbieter (``openai``, ``gemini``): Der erste Indexer-Lauf embedded den gesamten
vorhandenen Korpus in einem Durchgang und verursacht dafür die gesamten Kosten auf einmal. Setzen
Sie ``content_chunker.job.max_documents_per_run`` auf einen endlichen Wert, um diese Kosten
stattdessen auf mehrere Läufe zu verteilen.

Referenzen
============

- :doc:`rank-fusion` - Konfiguration von Rank Fusion (hybride Suche)
- :doc:`rag-chat` - Konfiguration des KI-Suchmodus
- :doc:`llm-overview` - Übersicht über die LLM-Integration
- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`setup-memory` - JVM-Speichereinstellungen
- :doc:`../install/upgrade` - Upgrade-Verfahren
